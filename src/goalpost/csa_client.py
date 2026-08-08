"""Faithful executor for target #2's three-stage screening chain
(upstream pinned in goalpost.upstream_csa; selection in
phase7/TARGET_SELECTION.md).

Mirrors the upstream `screening_agent.py` LLM wiring exactly:

1. extract prompt over the resume text (T=0.0);
2. score prompt over json.dumps(candidate_info, indent=2) and
   json.dumps(job_requirements, indent=2) (T=0.0);
3. recommend prompt over the info and scores dicts (T=0.3) — its output
   is the user-facing recommendation and the pipeline's verdict carrier.

Quirks mirrored deliberately: stage replies are fence-stripped then
json.loads'd, and a parse failure yields {} with the chain continuing;
per-stage temperatures/max_tokens are the upstream's own hardcoded values,
so the audit condition's temperature is recorded but never forwarded
(as-shipped behaviour).

Documented divergences (disclosed in the audit notes): plain-text CV input
instead of the OCR ingest stage; direct API calls instead of the LangGraph
harness (same prompts, order, and data flow); the PDF report stage is
omitted (local I/O, not model behaviour); served model is a declared
substitute — the upstream's pinned model is retired (upstream_csa).
"""

import json

from goalpost.pipeline_client import split_passthrough
from goalpost.upstream_csa import CSA_STAGE_PARAMS, csa_prompts, parse_json_reply

CSA_CLIENT_VERSION = "0.1.0"


class CSAPipelineClient:
    """Standard Goalpost client interface over the 3-stage chain. One
    `.complete()` = one full pipeline execution (3 provider calls); usage
    and cost are aggregated; the returned text is the recommendation
    stage's output. The `job_spec` slot of the passthrough prompt must
    carry the frozen job_requirements dict as JSON."""

    def __init__(self, inner):
        self.prompts = csa_prompts()
        self.inner = inner

    def _call(self, template: str, stage, seed: int, **slots):
        prompt = template
        for name, value in slots.items():
            prompt = prompt.replace("{" + name + "}", value)
        # upstream hardcodes per-stage max_tokens (2000/2000/1000); forward
        # them onto the inner client where it exposes the attribute
        if hasattr(self.inner, "max_tokens"):
            self.inner.max_tokens = stage.max_tokens
        return self.inner.complete(
            prompt=prompt, temperature=stage.temperature, seed=seed
        )

    def complete(self, prompt: str, temperature: float, seed: int) -> dict:
        # `temperature` is the condition's value; the upstream hardcodes
        # its own per-stage temperatures, which take precedence (as-shipped).
        cv, jd = split_passthrough(prompt)
        try:
            job_requirements = json.loads(jd)
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(
                "csa pipeline requires the job_spec slot to carry the "
                "frozen job_requirements dict as JSON"
            ) from exc
        if not isinstance(job_requirements, dict):
            raise ValueError(
                "csa pipeline job_requirements must be a JSON object"
            )

        extract_stage, score_stage, recommend_stage = CSA_STAGE_PARAMS

        r_extract = self._call(
            self.prompts.extract, extract_stage, seed, resume_text=cv
        )
        candidate_info = parse_json_reply(r_extract["text"])

        r_score = self._call(
            self.prompts.score, score_stage, seed,
            candidate_info=json.dumps(candidate_info, indent=2),
            job_requirements=json.dumps(job_requirements, indent=2),
        )
        scores = parse_json_reply(r_score["text"])

        r_recommend = self._call(
            self.prompts.recommend, recommend_stage, seed,
            candidate_info=json.dumps(candidate_info, indent=2),
            scores=json.dumps(scores, indent=2),
        )

        stages = [r_extract, r_score, r_recommend]
        return {
            "text": r_recommend["text"],
            "usage": {
                "input_tokens": sum(
                    s.get("usage", {}).get("input_tokens", 0) for s in stages
                ),
                "output_tokens": sum(
                    s.get("usage", {}).get("output_tokens", 0) for s in stages
                ),
            },
            "cost_usd": sum(s.get("cost_usd", 0.0) for s in stages),
            "model_fingerprint": r_recommend.get("model_fingerprint"),
            "pipeline_stages": len(stages),
        }
