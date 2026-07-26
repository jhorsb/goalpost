"""Faithful executor for the audited upstream 4-agent screening chain.

Mirrors the upstream `multi_agents.py` wiring exactly (plan:
peppy-gliding-steele), including its quirks, because the pipeline — not an
idealised version of it — is the system under test:

1. name-extract prompt over the resume text;
2. JD-requirements prompt over the job description, output
   **newline-stripped** (upstream does `.replace("\\n", "")`);
3. red-flag prompt over the resume text;
4. recruiter prompt whose "Job Description" slot receives
   `jd_output + " " + redflag_output` (upstream's `messages[-2:]` join —
   red flags ride along inside the JD slot).

Documented divergences from upstream (disclosed in the audit notes):
plain-text CV input instead of PyPDFLoader; direct API calls instead of
the LangChain/LangGraph harness (same prompts, order, and data flow);
served model is the pinned model's successor where the original is retired.
"""

from goalpost.upstream import UpstreamPrompts

PIPELINE_CLIENT_VERSION = "0.1.0"

_CV_MARK = "<<<CV>>>"
_JD_MARK = "<<<JD>>>"


def build_passthrough_template() -> str:
    """SUT prompt template that simply carries the case into the chain."""
    return f"{_CV_MARK}\n{{cv}}\n{_JD_MARK}\n{{job_spec}}"


def split_passthrough(prompt: str) -> tuple[str, str]:
    if _CV_MARK not in prompt or _JD_MARK not in prompt:
        raise ValueError("pipeline passthrough prompt missing CV/JD markers")
    _, rest = prompt.split(_CV_MARK, 1)
    cv, jd = rest.split(_JD_MARK, 1)
    return cv.strip("\n"), jd.strip("\n")


class UpstreamPipelineClient:
    """Standard Goalpost client interface over the upstream chain. One
    `.complete()` = one full pipeline execution (4 provider calls);
    usage and cost are aggregated; the returned text is the recruiter
    agent's output — the pipeline's user-facing verdict."""

    def __init__(self, prompts: UpstreamPrompts, inner):
        self.prompts = prompts
        self.inner = inner

    def _call(self, template: str, temperature: float, seed: int, **slots):
        prompt = template
        for name, value in slots.items():
            prompt = prompt.replace("{" + name + "}", value)
        return self.inner.complete(
            prompt=prompt, temperature=temperature, seed=seed
        )

    def complete(self, prompt: str, temperature: float, seed: int) -> dict:
        cv, jd = split_passthrough(prompt)

        r_name = self._call(
            self.prompts.name_extract, temperature, seed, resume_text=cv
        )
        r_jd = self._call(
            self.prompts.jd_extract, temperature, seed, jd_data=jd
        )
        jd_output = r_jd["text"].replace("\n", "")  # upstream quirk
        r_flags = self._call(
            self.prompts.redflag, temperature, seed, resume_text=cv
        )
        # upstream quirk: recruiter's JD slot = jd output + " " + red flags
        jd_data = jd_output + " " + r_flags["text"]
        r_final = self._call(
            self.prompts.recruiter, temperature, seed,
            resume_text=cv, jd_data=jd_data,
        )

        stages = [r_name, r_jd, r_flags, r_final]
        return {
            "text": r_final["text"],
            "usage": {
                "input_tokens": sum(
                    s.get("usage", {}).get("input_tokens", 0) for s in stages
                ),
                "output_tokens": sum(
                    s.get("usage", {}).get("output_tokens", 0) for s in stages
                ),
            },
            "cost_usd": sum(s.get("cost_usd", 0.0) for s in stages),
            "model_fingerprint": r_final.get("model_fingerprint"),
            "pipeline_stages": len(stages),
        }
