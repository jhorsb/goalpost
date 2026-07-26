"""Provider-agnostic endpoints (north star: audit any model, any lab, any
local runtime — no single-vendor dependency).

- `openai_compatible` provider with base_url + per-SUT api_key_env covers
  OpenRouter/Together/Groq/Mistral/DeepSeek/xAI/Ollama/vLLM/...
- base_url joins SUT identity (same model name on two endpoints is two SUTs)
- canonicaliser/extractor accept full endpoint specs (string stays accepted)
- pricing overrides let local/free endpoints cost zero instead of the
  conservative unknown-model default
"""

import pytest

from goalpost.config import AuditConfig, Condition, ModelEndpoint, SUTConfig
from goalpost.providers import compute_cost, make_client


def make_sut(**overrides):
    defaults = dict(
        name="screener",
        provider="openai_compatible",
        model="llama3.1:8b",
        base_url="http://localhost:11434/v1",
        api_key_env="OLLAMA_API_KEY",
        elicitation_mode="structured",
        prompt_template="CV: {cv} Spec: {job_spec}",
    )
    defaults.update(overrides)
    return SUTConfig(**defaults)


# ── endpoint identity ────────────────────────────────────────────────

def test_base_url_is_part_of_sut_identity():
    a = make_sut(base_url="https://openrouter.ai/api/v1")
    b = make_sut(base_url="https://api.together.xyz/v1")
    assert a.sut_id != b.sut_id


def test_native_providers_need_no_base_url():
    sut = make_sut(provider="anthropic", model="claude-haiku-4-5-20251001",
                   base_url=None, api_key_env=None)
    assert sut.sut_id


# ── config-level endpoint specs ──────────────────────────────────────

def config_kwargs(**overrides):
    kwargs = dict(
        audit_id="a",
        suts=[make_sut()],
        conditions=[Condition(temperature=0.0, repeats=2)],
        canonicaliser=ModelEndpoint(
            provider="openai_compatible",
            model="qwen2.5:7b",
            base_url="http://localhost:11434/v1",
        ),
        extractor=ModelEndpoint(
            provider="openai_compatible",
            model="qwen2.5:7b",
            base_url="http://localhost:11434/v1",
        ),
        max_spend_usd=0.5,
        audit_seed=42,
    )
    kwargs.update(overrides)
    return kwargs


def test_endpoint_objects_accepted_for_canonicaliser_and_extractor():
    config = AuditConfig(**config_kwargs())
    assert config.canonicaliser.model == "qwen2.5:7b"
    assert config.extractor.base_url.startswith("http://localhost")


def test_plain_string_still_accepted_and_coerced():
    config = AuditConfig(
        **config_kwargs(
            canonicaliser="claude-sonnet-4-5-20250929",
            extractor="gpt-4o-mini-2024-07-18",
        )
    )
    assert config.canonicaliser.provider == "anthropic"
    assert config.extractor.provider == "openai"


def test_canonicaliser_sharing_sut_model_still_hard_error():
    from goalpost.config import ConfigError

    with pytest.raises(ConfigError, match="canonicaliser"):
        AuditConfig(
            **config_kwargs(
                canonicaliser=ModelEndpoint(
                    provider="openai_compatible",
                    model="llama3.1:8b",  # same as the SUT
                    base_url="http://localhost:11434/v1",
                )
            )
        )


# ── client construction ──────────────────────────────────────────────

def test_make_client_openai_compatible_uses_base_url_and_key_env(monkeypatch):
    monkeypatch.setenv("MY_ROUTER_KEY", "sk-test-123")
    client = make_client(
        ModelEndpoint(
            provider="openai_compatible",
            model="meta-llama/llama-3.1-8b-instruct",
            base_url="https://openrouter.ai/api/v1",
            api_key_env="MY_ROUTER_KEY",
        )
    )
    assert str(client._client.base_url).startswith("https://openrouter.ai")
    assert client._client.api_key == "sk-test-123"


def test_make_client_openai_compatible_missing_key_defaults_to_placeholder(
    monkeypatch,
):
    # Local endpoints (Ollama, vLLM) need no key; client must still construct.
    monkeypatch.delenv("UNSET_KEY_VAR", raising=False)
    client = make_client(
        ModelEndpoint(
            provider="openai_compatible",
            model="llama3.1:8b",
            base_url="http://localhost:11434/v1",
            api_key_env="UNSET_KEY_VAR",
        )
    )
    assert client._client.api_key  # placeholder, not empty


# ── pricing overrides ────────────────────────────────────────────────

def test_pricing_override_beats_default():
    assert compute_cost(
        "llama3.1:8b", input_tokens=1_000_000, output_tokens=0,
        overrides={"llama3.1:8b": {"input": 0.0, "output": 0.0}},
    ) == 0.0


def test_unknown_model_without_override_stays_conservative():
    assert compute_cost("mystery-model", input_tokens=1000, output_tokens=0) > 0


def test_config_carries_pricing_overrides():
    config = AuditConfig(
        **config_kwargs(pricing={"llama3.1:8b": {"input": 0.0, "output": 0.0}})
    )
    assert config.pricing["llama3.1:8b"]["input"] == 0.0


def test_send_seed_false_omits_seed_from_request(monkeypatch):
    # Some OpenAI-compatible shims (Google AI Studio) reject `seed`.
    monkeypatch.setenv("X_KEY", "sk-test")
    endpoint = ModelEndpoint(
        provider="openai_compatible", model="gemini-2.5-flash",
        base_url="https://example.invalid/v1", api_key_env="X_KEY",
        send_seed=False,
    )
    client = make_client(endpoint)
    captured = {}

    class FakeCompletions:
        def create(self, **kwargs):
            captured.update(kwargs)
            raise RuntimeError("stop before network")

    client._client.chat.completions = FakeCompletions()
    try:
        client.complete(prompt="p", temperature=0.0, seed=123)
    except RuntimeError:
        pass
    assert "seed" not in captured
    assert captured["model"] == "gemini-2.5-flash"


def test_send_seed_defaults_true(monkeypatch):
    monkeypatch.setenv("X_KEY", "sk-test")
    endpoint = ModelEndpoint(
        provider="openai", model="gpt-4o-mini-2024-07-18", api_key_env="X_KEY"
    )
    client = make_client(endpoint)
    captured = {}

    class FakeCompletions:
        def create(self, **kwargs):
            captured.update(kwargs)
            raise RuntimeError("stop")

    client._client.chat.completions = FakeCompletions()
    try:
        client.complete(prompt="p", temperature=0.0, seed=123)
    except RuntimeError:
        pass
    assert captured.get("seed") == 123
