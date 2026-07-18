"""Runner core (never-delegate — DESIGN.md §7/§9).

Integrity guarantees enforced here:
- per-repetition seeds derived deterministically and recorded;
- cache key includes case/variant hash + repetition_index, so repeats are
  never cache hits;
- budget enforced at block boundaries only (block = all N repeats of one
  SUT × condition × case) — no partial blocks;
- breadth-balanced interleaving across SUTs, so a mid-audit budget stop
  leaves comparable coverage per SUT;
- resume = re-run over the missing-blocks list only.
"""

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from goalpost.config import Case, Condition, SUTConfig

RUNNER_VERSION = "0.1.0"


def _sha256_int(*parts) -> int:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(str(part).encode("utf-8"))
        digest.update(b"\x1f")
    # Providers require seeds within signed int64 (OpenAI rejects above
    # 2^63-1) — mask to 63 bits. Found by the first live run.
    return int.from_bytes(digest.digest()[:8], "big") & (2**63 - 1)


def derive_seed(
    audit_seed: int,
    sut_id: str,
    condition_id: str,
    case_hash: str,
    repetition_index: int,
) -> int:
    return _sha256_int(audit_seed, sut_id, condition_id, case_hash, repetition_index)


def cache_key(
    *,
    provider: str,
    model: str,
    params: str,
    prompt: str,
    temperature: float,
    case_hash: str,
    repetition_index: int,
) -> str:
    digest = hashlib.sha256()
    for part in (provider, model, params, prompt, temperature, case_hash, repetition_index):
        digest.update(str(part).encode("utf-8"))
        digest.update(b"\x1f")
    return digest.hexdigest()


class CallCache:
    """Content-addressed on-disk response cache."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self.root / f"{key}.json"

    def get(self, key: str):
        path = self._path(key)
        if not path.exists():
            return None
        return json.loads(path.read_text())

    def put(self, key: str, value: dict) -> None:
        self._path(key).write_text(json.dumps(value))


@dataclass(frozen=True)
class Block:
    sut: SUTConfig
    condition: Condition
    case: Case

    @property
    def block_id(self) -> str:
        return f"{self.sut.sut_id}/{self.condition.condition_id}/{self.case.case_id}"


@dataclass
class RunResult:
    transcripts: list[dict] = field(default_factory=list)
    completed_blocks: list[Block] = field(default_factory=list)
    missing_blocks: list[Block] = field(default_factory=list)
    total_cost_usd: float = 0.0


def plan_blocks(
    suts: list[SUTConfig], conditions: list[Condition], cases: list[Case]
) -> list[Block]:
    """Breadth-balanced: iterate condition × case in the outer loops and
    SUTs innermost, so every SUT covers the same ground before any SUT
    pulls ahead."""
    return [
        Block(sut=sut, condition=condition, case=case)
        for condition in conditions
        for case in cases
        for sut in suts
    ]


def run_audit_blocks(
    blocks: list[Block],
    *,
    client_factory,
    cache: CallCache,
    audit_seed: int,
    max_spend_usd: float,
) -> RunResult:
    result = RunResult()

    for block in blocks:
        # Budget check at the block boundary: estimate from observed mean
        # cost per call so far; before any spend, attempt the block.
        calls_so_far = len(result.transcripts)
        if calls_so_far:
            estimated_block_cost = (
                result.total_cost_usd / calls_so_far
            ) * block.condition.repeats
            if result.total_cost_usd + estimated_block_cost > max_spend_usd:
                result.missing_blocks.append(block)
                continue

        client = client_factory(block.sut)
        # Replace-based substitution, not str.format: operator templates and
        # the appended output contract legitimately contain JSON braces.
        prompt = block.sut.prompt_template.replace(
            "{cv}", block.case.cv_text
        ).replace("{job_spec}", block.case.job_spec_text)
        block_transcripts = []
        for repetition_index in range(block.condition.repeats):
            seed = derive_seed(
                audit_seed,
                block.sut.sut_id,
                block.condition.condition_id,
                block.case.content_hash,
                repetition_index,
            )
            key = cache_key(
                provider=block.sut.provider,
                model=block.sut.model,
                params=repr(sorted(block.sut.params.items())),
                prompt=prompt,
                temperature=block.condition.temperature,
                case_hash=block.case.content_hash,
                repetition_index=repetition_index,
            )
            cached = cache.get(key)
            if cached is not None:
                response, from_cache = cached, True
            else:
                response = client.complete(
                    prompt=prompt,
                    temperature=block.condition.temperature,
                    seed=seed,
                )
                cache.put(key, response)
                from_cache = False

            block_transcripts.append(
                {
                    "transcript_id": key[:24],
                    "sut_id": block.sut.sut_id,
                    "condition_id": block.condition.condition_id,
                    "case_id": block.case.case_id,
                    "case_hash": block.case.content_hash,
                    "repetition_index": repetition_index,
                    "prompt": prompt,
                    "response_text": response["text"],
                    "usage": response.get("usage", {}),
                    "cost_usd": 0.0 if from_cache else response.get("cost_usd", 0.0),
                    "provider_seed": seed,
                    "model_fingerprint": response.get("model_fingerprint"),
                    "from_cache": from_cache,
                    "runner_version": RUNNER_VERSION,
                }
            )

        result.transcripts.extend(block_transcripts)
        result.total_cost_usd += sum(t["cost_usd"] for t in block_transcripts)
        result.completed_blocks.append(block)

    return result
