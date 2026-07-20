"""Runner core: seed derivation, cache identity, block scheduling, budget
stops, resume. Never-delegate module; the named regression tests here are
required by DESIGN.md §7/§8 ("glassware is delegable, protocol isn't")."""

import pytest
from goalpost.config import Case, Condition, SUTConfig
from goalpost.runner import (
    Block,
    CallCache,
    cache_key,
    derive_seed,
    plan_blocks,
    run_audit_blocks,
)


def sut(name="screener", mode="structured"):
    return SUTConfig(
        name=name,
        provider="fake",
        model=f"fake-model-{name}-2026-01-01",
        elicitation_mode=mode,
        prompt_template="CV: {cv}\nSpec: {job_spec}",
    )


CASE = Case(case_id="c1", cv_text="a cv", job_spec_text="a spec")
CASE2 = Case(case_id="c2", cv_text="other cv", job_spec_text="other spec")
COND = Condition(temperature=0.0, repeats=3)


# ── seed derivation (named regression: seed-per-repetition) ──────────

def test_seed_deterministic_for_same_inputs():
    a = derive_seed(42, "sut1", "t0.0_n3", "hash1", 0)
    b = derive_seed(42, "sut1", "t0.0_n3", "hash1", 0)
    assert a == b


def test_regression_seed_differs_per_repetition():
    seeds = {derive_seed(42, "sut1", "t0.0_n3", "hash1", i) for i in range(5)}
    assert len(seeds) == 5


def test_seed_differs_across_audit_seeds():
    assert derive_seed(1, "s", "c", "h", 0) != derive_seed(2, "s", "c", "h", 0)


# ── cache identity (named regression: repeats never cache hits) ──────

def test_regression_cache_key_differs_per_repetition():
    base = dict(
        provider="fake", model="m", params="{}", prompt="p",
        temperature=0.0, case_hash="h",
    )
    assert cache_key(**base, repetition_index=0) != cache_key(
        **base, repetition_index=1
    )


def test_cache_key_stable_for_identical_call():
    kwargs = dict(
        provider="fake", model="m", params="{}", prompt="p",
        temperature=0.0, case_hash="h", repetition_index=2,
    )
    assert cache_key(**kwargs) == cache_key(**kwargs)


def test_cache_roundtrip(tmp_path):
    cache = CallCache(tmp_path)
    key = "abc123"
    assert cache.get(key) is None
    cache.put(key, {"text": "hello", "cost_usd": 0.001})
    assert cache.get(key) == {"text": "hello", "cost_usd": 0.001}


# ── block planning: breadth-balanced interleaving ────────────────────

def test_plan_blocks_one_block_per_sut_condition_case():
    blocks = plan_blocks([sut("a"), sut("b")], [COND], [CASE, CASE2])
    assert len(blocks) == 4
    assert all(isinstance(b, Block) for b in blocks)


def test_plan_blocks_interleaves_suts_breadth_first():
    blocks = plan_blocks([sut("a"), sut("b")], [COND], [CASE, CASE2])
    sut_order = [b.sut.name for b in blocks]
    # breadth-balanced: alternating, never all of one SUT first
    assert sut_order[:2] in (["a", "b"], ["b", "a"])
    assert sut_order[2:] in (["a", "b"], ["b", "a"])


# ── budget stops at block boundaries ─────────────────────────────────

class FakeClient:
    """Deterministic fake provider client; cost fixed per call."""

    def __init__(self, cost_per_call=0.01, text="DECISION_JSON: {\"decision\": {\"label\": \"reject\"}}\nREASONS_JSON: {\"reasons\": []}\nRECOURSE_JSON: {\"actions\": []}"):
        self.cost_per_call = cost_per_call
        self.text = text
        self.calls = []

    def complete(self, prompt, temperature, seed):
        self.calls.append({"prompt": prompt, "temperature": temperature, "seed": seed})
        return {
            "text": self.text,
            "usage": {"input_tokens": 10, "output_tokens": 10},
            "cost_usd": self.cost_per_call,
            "model_fingerprint": "fake-fp-1",
        }


def test_regression_budget_stops_at_block_boundary_never_mid_block(tmp_path):
    client = FakeClient(cost_per_call=0.01)
    blocks = plan_blocks([sut("a")], [COND], [CASE, CASE2])  # 2 blocks × 3 calls
    # budget allows first block (0.03) but not both (0.06)
    result = run_audit_blocks(
        blocks,
        client_factory=lambda s: client,
        cache=CallCache(tmp_path),
        audit_seed=42,
        max_spend_usd=0.04,
    )
    assert len(result.completed_blocks) == 1
    assert len(result.missing_blocks) == 1
    # the completed block ran all its repeats; nothing partial
    assert len(result.transcripts) == COND.repeats
    assert result.total_cost_usd == 0.03


def test_transcripts_carry_lineage_keys(tmp_path):
    client = FakeClient()
    blocks = plan_blocks([sut("a")], [COND], [CASE])
    result = run_audit_blocks(
        blocks,
        client_factory=lambda s: client,
        cache=CallCache(tmp_path),
        audit_seed=42,
        max_spend_usd=1.0,
    )
    reps = sorted(t["repetition_index"] for t in result.transcripts)
    assert reps == [0, 1, 2]
    assert all(t["case_hash"] == CASE.content_hash for t in result.transcripts)
    assert all(t["condition_id"] == COND.condition_id for t in result.transcripts)
    assert all(t["provider_seed"] is not None for t in result.transcripts)
    # per-repetition seeds all distinct (regression pairing with derive_seed)
    assert len({t["provider_seed"] for t in result.transcripts}) == 3


def test_resume_fills_only_missing_blocks(tmp_path):
    cache = CallCache(tmp_path)
    blocks = plan_blocks([sut("a")], [COND], [CASE, CASE2])
    first = run_audit_blocks(
        blocks, client_factory=lambda s: FakeClient(),
        cache=cache, audit_seed=42, max_spend_usd=0.04,
    )
    assert len(first.missing_blocks) == 1
    client2 = FakeClient()
    second = run_audit_blocks(
        first.missing_blocks, client_factory=lambda s: client2,
        cache=cache, audit_seed=42, max_spend_usd=1.0,
    )
    assert len(second.completed_blocks) == 1
    assert len(client2.calls) == COND.repeats  # only the missing block ran


def test_seed_fits_signed_int64_provider_requirement():
    # OpenAI (and most providers) reject seeds above 2^63-1; sha256-derived
    # seeds must stay within signed-int64 range. Found by the first live run.
    seeds = [
        derive_seed(42, f"sut{i}", "t0.0_n5", f"hash{i}", i) for i in range(200)
    ]
    assert all(0 <= s <= 2**63 - 1 for s in seeds)
    assert len(set(seeds)) == 200  # still distinct


# ── bounded concurrency within blocks ────────────────────────────────

def test_concurrent_block_preserves_order_and_seeds(tmp_path):
    client = FakeClient()
    blocks = plan_blocks([sut("a")], [Condition(temperature=0.0, repeats=5)], [CASE])
    result = run_audit_blocks(
        blocks, client_factory=lambda s: client, cache=CallCache(tmp_path),
        audit_seed=42, max_spend_usd=1.0, concurrency=3,
    )
    reps = [t["repetition_index"] for t in result.transcripts]
    assert reps == [0, 1, 2, 3, 4]
    assert len({t["provider_seed"] for t in result.transcripts}) == 5
    assert result.total_cost_usd == pytest.approx(0.05)


def test_concurrency_actually_overlaps_calls(tmp_path):
    import threading
    import time as time_mod

    class SlowClient(FakeClient):
        def __init__(self):
            super().__init__()
            self.lock = threading.Lock()
            self.active = 0
            self.max_active = 0

        def complete(self, prompt, temperature, seed):
            with self.lock:
                self.active += 1
                self.max_active = max(self.max_active, self.active)
            time_mod.sleep(0.05)
            try:
                return super().complete(prompt, temperature, seed)
            finally:
                with self.lock:
                    self.active -= 1

    client = SlowClient()
    blocks = plan_blocks([sut("a")], [Condition(temperature=0.0, repeats=4)], [CASE])
    run_audit_blocks(
        blocks, client_factory=lambda s: client, cache=CallCache(tmp_path),
        audit_seed=42, max_spend_usd=1.0, concurrency=4,
    )
    assert client.max_active >= 2

