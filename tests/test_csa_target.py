"""Target #2 mirror: the MIT-licensed LangGraph candidate-screening agent
(phase7/TARGET_SELECTION.md; upstream pinned in goalpost.upstream_csa).

Mirrors the upstream's three LLM stages exactly, quirks included:
1. extract_candidate_info(resume_text)          T=0.0, max_tokens 2000
2. score_candidate(info, job_requirements)      T=0.0, max_tokens 2000
3. generate_recommendation(info, scores)        T=0.3, max_tokens 1000

Quirks under test:
- stage outputs are parsed as JSON after stripping ``` fences; a parse
  failure yields {} and the chain CONTINUES with the empty dict;
- stages 2/3 receive json.dumps(..., indent=2) of the prior stage's dict;
- temperatures are the upstream's own hardcoded per-stage values — the
  condition temperature is recorded but never forwarded (as-shipped).
"""

import json

import pytest

from goalpost.csa_client import CSAPipelineClient
from goalpost.upstream_csa import (
    CSA_STAGE_PARAMS,
    PINNED_CSA,
    csa_prompts,
    parse_json_reply,
)


class RecordingInner:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []
        self.max_tokens = 9999

    def complete(self, prompt, temperature, seed):
        self.calls.append(
            {"prompt": prompt, "temperature": temperature, "seed": seed,
             "max_tokens": self.max_tokens}
        )
        n = len(self.calls)
        return {
            "text": self.replies[n - 1],
            "usage": {"input_tokens": 10 * n, "output_tokens": n},
            "cost_usd": 0.001 * n,
            "model_fingerprint": "claude-fp",
        }


JOB_REQS = {"title": "Senior Software Engineer", "required_skills": ["Python"]}
INFO_JSON = '{"summary": "seasoned engineer", "skills": {"technical": ["Python"]}}'
SCORES_JSON = '{"overall_score": 82, "strengths": ["python depth"]}'
FINAL_TEXT = "Overall assessment: Yes\nStrengths...\nNext steps..."


def make_prompt(cv="MY CV"):
    from goalpost.pipeline_client import build_passthrough_template

    template = build_passthrough_template()
    return template.replace("{cv}", cv).replace(
        "{job_spec}", json.dumps(JOB_REQS)
    )


def make_client(replies=None):
    inner = RecordingInner(
        replies or [INFO_JSON, SCORES_JSON, FINAL_TEXT]
    )
    return CSAPipelineClient(inner=inner), inner


# ── upstream pin & prompts ───────────────────────────────────────────

def test_pin_identifies_upstream():
    assert PINNED_CSA.sha == "707e6abeb2c63d35323b772e68c4a824c59197b2"
    assert PINNED_CSA.content_sha256 == (
        "195eee21ddf7390366c685cf6a770c12a581dc3c96f83d371c9165f60687e936"
    )
    assert PINNED_CSA.license == "MIT"


def test_prompts_carry_upstream_schema_anchors():
    p = csa_prompts()
    assert "personal_info" in p.extract and "{resume_text}" in p.extract
    assert "overall_score" in p.score and "cultural_fit" in p.score
    assert "{candidate_info}" in p.score and "{job_requirements}" in p.score
    assert "Strong Yes, Yes, Maybe, No" in p.recommend
    assert "{candidate_info}" in p.recommend and "{scores}" in p.recommend


def test_prompts_render_single_braces_on_the_wire():
    # upstream's f-strings collapse {{ to {; the mirror must send the same
    p = csa_prompts()
    for template in (p.extract, p.score, p.recommend):
        assert "{{" not in template and "}}" not in template
    assert '"personal_info": {' in p.extract
    assert '"overall_score": 0-100' in p.score


def test_stage_params_mirror_upstream_hardcoding():
    assert [s.temperature for s in CSA_STAGE_PARAMS] == [0.0, 0.0, 0.3]
    assert [s.max_tokens for s in CSA_STAGE_PARAMS] == [2000, 2000, 1000]


# ── fence-strip JSON parse quirk ─────────────────────────────────────

def test_parse_json_reply_plain_and_fenced():
    assert parse_json_reply('{"a": 1}') == {"a": 1}
    assert parse_json_reply('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json_reply('```\n{"a": 1}\n```') == {"a": 1}


def test_parse_json_reply_failure_yields_empty_dict():
    assert parse_json_reply("I cannot produce JSON today.") == {}


# ── chain wiring ─────────────────────────────────────────────────────

def test_chain_runs_three_calls_with_faithful_wiring():
    client, inner = make_client()
    result = client.complete(prompt=make_prompt(), temperature=0.7, seed=1)

    assert len(inner.calls) == 3
    # stage 1 sees the resume text
    assert "MY CV" in inner.calls[0]["prompt"]
    # stage 2 sees stage 1's dict and the job requirements, both pretty-printed
    assert json.dumps(json.loads(INFO_JSON), indent=2) in inner.calls[1]["prompt"]
    assert json.dumps(JOB_REQS, indent=2) in inner.calls[1]["prompt"]
    # stage 3 sees the info dict and the scores dict
    assert json.dumps(json.loads(SCORES_JSON), indent=2) in inner.calls[2]["prompt"]
    # upstream hardcodes per-stage temperatures; condition T is not forwarded
    assert [c["temperature"] for c in inner.calls] == [0.0, 0.0, 0.3]
    # and per-stage max_tokens are forwarded onto the inner client
    assert [c["max_tokens"] for c in inner.calls] == [2000, 2000, 1000]

    assert result["text"] == FINAL_TEXT
    assert result["usage"]["input_tokens"] == 60
    assert result["usage"]["output_tokens"] == 6
    assert result["cost_usd"] == pytest.approx(0.006)
    assert result["model_fingerprint"] == "claude-fp"
    assert result["pipeline_stages"] == 3


def test_parse_failure_propagates_empty_dict_and_chain_continues():
    client, inner = make_client(
        replies=["NOT JSON AT ALL", SCORES_JSON, FINAL_TEXT]
    )
    result = client.complete(prompt=make_prompt(), temperature=0.0, seed=2)
    # upstream quirk: stage 1 failure -> {}; stage 2 still runs with "{}"
    assert json.dumps({}, indent=2) in inner.calls[1]["prompt"]
    assert result["text"] == FINAL_TEXT


def test_job_requirements_must_be_json():
    client, _ = make_client()
    from goalpost.pipeline_client import build_passthrough_template

    bad = build_passthrough_template().replace("{cv}", "CV").replace(
        "{job_spec}", "just prose, not a dict"
    )
    with pytest.raises(ValueError, match="job_requirements"):
        client.complete(prompt=bad, temperature=0.0, seed=3)


# ── CLI factory dispatch ─────────────────────────────────────────────

def test_client_factory_dispatches_csa_pipeline(monkeypatch):
    from goalpost.cli import make_sut_client
    from goalpost.config import SUTConfig
    from goalpost.pipeline_client import build_passthrough_template

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    sut = SUTConfig(
        name="csa", provider="anthropic",
        model="claude-haiku-4-5-20251001",
        elicitation_mode="freeform",
        prompt_template=build_passthrough_template(),
        params={"pipeline": "csa-screening-agent",
                "upstream_sha": PINNED_CSA.sha[:7]},
    )
    client = make_sut_client(sut, pricing={})
    assert isinstance(client, CSAPipelineClient)
