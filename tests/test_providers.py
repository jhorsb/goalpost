"""Provider adapters: response normalisation and cost computation.

Adapters wrap the official SDKs; the units under test are pure — SDK
response → canonical response dict, and usage × pricing table → cost.
No network anywhere in this file.
"""

import pytest

from goalpost.providers import (
    PRICING,
    compute_cost,
    normalise_anthropic_response,
    normalise_openai_response,
)


class Obj:
    """Attribute-access stub mirroring SDK response objects."""

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


def test_normalise_anthropic_response():
    resp = Obj(
        content=[Obj(type="text", text="DECISION_JSON: ...")],
        usage=Obj(input_tokens=100, output_tokens=50),
        model="claude-haiku-4-5-20251001",
        stop_reason="end_turn",
    )
    out = normalise_anthropic_response(resp)
    assert out["text"] == "DECISION_JSON: ..."
    assert out["usage"] == {"input_tokens": 100, "output_tokens": 50}
    assert out["model_fingerprint"] == "claude-haiku-4-5-20251001"
    assert out["stop_reason"] == "end_turn"
    assert out["cost_usd"] == pytest.approx(
        100 / 1e6 * PRICING["claude-haiku-4-5-20251001"]["input"]
        + 50 / 1e6 * PRICING["claude-haiku-4-5-20251001"]["output"]
    )


def test_normalise_anthropic_refusal_stop_reason_preserved():
    resp = Obj(
        content=[],
        usage=Obj(input_tokens=10, output_tokens=0),
        model="claude-haiku-4-5-20251001",
        stop_reason="refusal",
    )
    out = normalise_anthropic_response(resp)
    assert out["text"] == ""
    assert out["stop_reason"] == "refusal"


def test_normalise_openai_response():
    resp = Obj(
        choices=[Obj(message=Obj(content="hello"), finish_reason="stop")],
        usage=Obj(prompt_tokens=200, completion_tokens=80),
        model="gpt-4o-mini-2024-07-18",
        system_fingerprint="fp_abc",
    )
    out = normalise_openai_response(resp)
    assert out["text"] == "hello"
    assert out["usage"] == {"input_tokens": 200, "output_tokens": 80}
    assert out["model_fingerprint"] == "fp_abc"
    assert out["stop_reason"] == "stop"
    assert out["cost_usd"] > 0


def test_compute_cost_unknown_model_uses_conservative_default():
    # Unknown models must not silently cost zero — budget enforcement
    # depends on cost never being underestimated to nothing.
    cost = compute_cost("unknown-model-xyz", input_tokens=1000, output_tokens=1000)
    assert cost > 0


def test_compute_cost_known_model():
    cost = compute_cost(
        "claude-haiku-4-5-20251001", input_tokens=1_000_000, output_tokens=0
    )
    assert cost == pytest.approx(PRICING["claude-haiku-4-5-20251001"]["input"])


# ── reasoning models (gpt-oss, GLM): content may be absent ───────────

def test_normalise_openai_missing_content_is_empty_not_crash():
    """Reasoning models emit message.reasoning first; if the token budget
    is consumed before the answer, `content` is absent entirely. Must not
    crash, and must surface the cause rather than a silent empty string."""
    resp = Obj(
        choices=[Obj(message=Obj(reasoning="thinking..."), finish_reason="length")],
        usage=Obj(prompt_tokens=50, completion_tokens=30),
        model="gpt-oss-120b",
        system_fingerprint="fp_x",
    )
    out = normalise_openai_response(resp)
    assert out["text"] == ""
    assert out["stop_reason"] == "length"
    assert out["truncated_before_content"] is True


def test_normalise_openai_content_present_not_flagged_truncated():
    resp = Obj(
        choices=[Obj(message=Obj(content="real answer", reasoning="r"),
                     finish_reason="stop")],
        usage=Obj(prompt_tokens=50, completion_tokens=30),
        model="gpt-oss-120b",
        system_fingerprint="fp_x",
    )
    out = normalise_openai_response(resp)
    assert out["text"] == "real answer"
    assert out["truncated_before_content"] is False


def test_endpoint_max_tokens_honoured(monkeypatch):
    from goalpost.config import ModelEndpoint
    from goalpost.providers import make_client

    monkeypatch.setenv("K", "sk-test")
    client = make_client(
        ModelEndpoint(provider="openai_compatible", model="m",
                      base_url="https://x.invalid/v1", api_key_env="K",
                      max_tokens=3000)
    )
    assert client.max_tokens == 3000
