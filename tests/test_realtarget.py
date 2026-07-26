"""Real-target machinery: runtime-fetched upstream pipeline (never
committed), hash verification, ast-only prompt extraction, faithful
4-call chain client, CLI dispatch. Plan: peppy-gliding-steele."""

import hashlib
import textwrap

import pytest

from goalpost.upstream import (
    UpstreamPin,
    UpstreamVerificationError,
    extract_prompts,
    verify_source,
)

# Structural mimic of the upstream file: OUR text, same AST shape
# (4 functions, f-string prompts over resume_text/jd_data, one
# newline-strip quirk). Not the upstream's copyrighted text.
MIMIC = textwrap.dedent('''
    llm = SomeLLM(model="some-model")

    def agent(state):
        resume_text = load()
        response = llm.invoke(
            f"Step one alpha. Resume Data: {resume_text}"
        )
        return {"messages": [response.content]}

    def JD_agent(state):
        jd_data = read()
        response = llm.invoke(
            f"Step two bravo. Data: {jd_data}"
        )
        result = response.content.replace("\\n", "")
        return {"messages": [result]}

    def redflag_agent(state):
        resume_text = load()
        prompt = f"""
        Step three charlie.
        Resume Data: {resume_text}
        """
        response = llm.invoke(prompt)
        return {"messages": [response.content]}

    def recruit_agent(state):
        resume_text = load()
        messages = state['messages']
        jd_data = str(messages[-2]) + " " + str(messages[-1])
        prompt = f"""
        Step four delta.
        Resume Data:
        {resume_text}
        Job Description:
        {jd_data}
        """
        response = llm.invoke(prompt)
        return {"messages": [response.content]}
''')


def test_extract_prompts_finds_all_four_with_placeholders():
    prompts = extract_prompts(MIMIC)
    assert "Step one alpha" in prompts.name_extract
    assert "{resume_text}" in prompts.name_extract
    assert "Step two bravo" in prompts.jd_extract
    assert "{jd_data}" in prompts.jd_extract
    assert "Step three charlie" in prompts.redflag
    assert "Step four delta" in prompts.recruiter
    assert "{resume_text}" in prompts.recruiter
    assert "{jd_data}" in prompts.recruiter


def test_extract_never_executes_source():
    evil = MIMIC + '\nimport os\nos.environ["PWNED"] = "1"\n'
    import os

    extract_prompts(evil)
    assert "PWNED" not in os.environ


def test_verify_source_hash_mismatch_hard_fails():
    pin = UpstreamPin(
        repo="example/repo", path="f.py", sha="abc",
        content_sha256=hashlib.sha256(b"expected").hexdigest(),
    )
    verify_source("expected", pin)  # ok
    with pytest.raises(UpstreamVerificationError):
        verify_source("tampered", pin)


# ── chain client ─────────────────────────────────────────────────────

from goalpost.pipeline_client import (  # noqa: E402
    UpstreamPipelineClient,
    build_passthrough_template,
    split_passthrough,
)


class RecordingInner:
    def __init__(self):
        self.calls = []

    def complete(self, prompt, temperature, seed):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        n = len(self.calls)
        return {
            "text": f"OUT{n}\nline2",
            "usage": {"input_tokens": 10 * n, "output_tokens": n},
            "cost_usd": 0.001 * n,
            "model_fingerprint": "llama-fp",
        }


def make_client():
    prompts = extract_prompts(MIMIC)
    inner = RecordingInner()
    return UpstreamPipelineClient(prompts=prompts, inner=inner), inner


def test_passthrough_roundtrip():
    template = build_passthrough_template()
    prompt = template.replace("{cv}", "CV TEXT").replace("{job_spec}", "JD TEXT")
    cv, jd = split_passthrough(prompt)
    assert cv == "CV TEXT" and jd == "JD TEXT"


def test_chain_runs_four_calls_with_faithful_wiring():
    client, inner = make_client()
    template = build_passthrough_template()
    prompt = template.replace("{cv}", "MY CV").replace("{job_spec}", "MY JD")
    result = client.complete(prompt=prompt, temperature=0.7, seed=1)

    assert len(inner.calls) == 4
    assert "MY CV" in inner.calls[0]["prompt"]          # name extract
    assert "MY JD" in inner.calls[1]["prompt"]          # jd extract
    assert "MY CV" in inner.calls[2]["prompt"]          # redflag
    # recruiter: resume + (jd output newline-stripped + " " + redflag output)
    recruiter_prompt = inner.calls[3]["prompt"]
    assert "MY CV" in recruiter_prompt
    assert "OUT2line2 OUT3\nline2" in recruiter_prompt  # upstream quirks
    assert all(c["temperature"] == 0.7 for c in inner.calls)

    # final output is the recruiter's, usage/cost aggregated
    assert result["text"] == "OUT4\nline2"
    assert result["usage"]["input_tokens"] == 100
    assert result["cost_usd"] == pytest.approx(0.010)
    assert result["model_fingerprint"] == "llama-fp"


# ── CLI factory dispatch ─────────────────────────────────────────────

def test_client_factory_dispatches_pipeline_suts(monkeypatch):
    from goalpost.cli import make_sut_client
    from goalpost.config import SUTConfig
    from goalpost import upstream as upstream_mod

    monkeypatch.setattr(
        upstream_mod, "load_upstream_prompts", lambda pin: extract_prompts(MIMIC)
    )
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    sut = SUTConfig(
        name="hs", provider="openai_compatible",
        model="llama-3.3-70b-versatile",
        base_url="https://api.groq.com/openai/v1",
        api_key_env="GROQ_API_KEY",
        elicitation_mode="freeform",
        prompt_template=build_passthrough_template(),
        params={"pipeline": "hs-resume-screener", "upstream_sha": "49dc41a"},
    )
    client = make_sut_client(sut, pricing={})
    assert isinstance(client, UpstreamPipelineClient)


def test_client_factory_plain_suts_unchanged(monkeypatch):
    from goalpost.cli import make_sut_client
    from goalpost.config import SUTConfig
    from goalpost.providers import OpenAICompatibleClient

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    sut = SUTConfig(
        name="plain", provider="openai", model="gpt-4o-mini-2024-07-18",
        elicitation_mode="structured", prompt_template="CV {cv} {job_spec}",
    )
    assert isinstance(make_sut_client(sut, pricing={}), OpenAICompatibleClient)
