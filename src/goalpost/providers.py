"""Provider adapters over the official SDKs (anthropic, openai).

The SDK call itself is a thin shell; everything testable is pure:
response normalisation into the canonical response dict the runner
expects, and cost computation from the committed pricing table.
Unit tests never touch the network (kickoff §8).
"""

import os

PROVIDERS_VERSION = "0.1.0"

# USD per 1M tokens. Committed and versioned; verified against provider
# pricing pages at build time (claude-api reference, 2026-07-05). Estimates
# feed --dry-run and budget enforcement; actual spend is computed from
# returned usage against this same table and recorded per transcript.
PRICING: dict[str, dict[str, float]] = {
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
    "claude-sonnet-4-5-20250929": {"input": 3.00, "output": 15.00},
    "gpt-4o-mini-2024-07-18": {"input": 0.15, "output": 0.60},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}

# Budget enforcement must never underestimate an unknown model to zero:
# assume mid-tier pricing when the model is not in the table.
_DEFAULT_PRICING = {"input": 5.00, "output": 25.00}


def compute_cost(
    model: str,
    *,
    input_tokens: int,
    output_tokens: int,
    overrides: dict[str, dict[str, float]] | None = None,
) -> float:
    """Config-supplied overrides beat the committed table; unknown models
    without an override stay conservatively priced (never free by accident —
    local/free endpoints declare 0.0 explicitly)."""
    rates = (overrides or {}).get(model) or PRICING.get(model, _DEFAULT_PRICING)
    return (
        input_tokens / 1e6 * rates["input"]
        + output_tokens / 1e6 * rates["output"]
    )


def normalise_anthropic_response(resp, overrides=None) -> dict:
    text = "".join(
        block.text for block in resp.content if getattr(block, "type", "") == "text"
    )
    usage = {
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
    }
    return {
        "text": text,
        "usage": usage,
        "cost_usd": compute_cost(resp.model, **usage, overrides=overrides),
        "model_fingerprint": resp.model,
        "stop_reason": resp.stop_reason,
    }


def normalise_openai_response(resp, overrides=None) -> dict:
    choice = resp.choices[0]
    usage = {
        "input_tokens": resp.usage.prompt_tokens,
        "output_tokens": resp.usage.completion_tokens,
    }
    text = getattr(choice.message, "content", None) or ""
    # Reasoning models (gpt-oss, GLM, ...) stream `reasoning` before the
    # answer; if the token budget runs out first there is no content at
    # all. Flag it so it reads as a truncation, not a silent empty answer.
    truncated = bool(
        not text
        and getattr(choice.message, "reasoning", None)
    )
    return {
        "text": text,
        "usage": usage,
        "cost_usd": compute_cost(resp.model, **usage, overrides=overrides),
        "model_fingerprint": getattr(resp, "system_fingerprint", None) or resp.model,
        "stop_reason": choice.finish_reason,
        "truncated_before_content": truncated,
    }


def _resolve_key(endpoint, default_env: str) -> str | None:
    """Named env var wins; fall back to the provider's conventional var;
    local OpenAI-compatible endpoints get a placeholder (the wire format
    requires a non-empty key even when the server ignores it)."""
    if getattr(endpoint, "api_key_env", None):
        key = os.environ.get(endpoint.api_key_env)
        if key:
            return key
    key = os.environ.get(default_env)
    if key:
        return key
    return None


class AnthropicClient:
    """Live client. Constructed lazily so offline tests never import creds."""

    def __init__(self, endpoint, max_tokens: int | None = None, pricing=None):
        import anthropic

        max_tokens = max_tokens or getattr(endpoint, "max_tokens", None) or 2048

        kwargs = {}
        key = _resolve_key(endpoint, "ANTHROPIC_API_KEY")
        if key:
            kwargs["api_key"] = key
        if getattr(endpoint, "base_url", None):
            kwargs["base_url"] = endpoint.base_url
        self._client = anthropic.Anthropic(**kwargs)
        self.model = endpoint.model
        self.max_tokens = max_tokens
        self.pricing = pricing

    def complete(self, prompt: str, temperature: float, seed: int) -> dict:
        # The Messages API has no sampling-seed parameter; the derived seed
        # is recorded in the transcript for provenance but cannot be passed.
        resp = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return normalise_anthropic_response(resp, overrides=self.pricing)


class OpenAICompatibleClient:
    """OpenAI itself, or any endpoint speaking its wire shape: OpenRouter,
    Together, Groq, Mistral, DeepSeek, xAI, Ollama, vLLM, LM Studio, ..."""

    def __init__(self, endpoint, max_tokens: int | None = None, pricing=None):
        import openai

        max_tokens = max_tokens or getattr(endpoint, "max_tokens", None) or 2048
        key = _resolve_key(endpoint, "OPENAI_API_KEY") or "not-needed"
        kwargs = {"api_key": key}
        if getattr(endpoint, "base_url", None):
            kwargs["base_url"] = endpoint.base_url
        self._client = openai.OpenAI(**kwargs)
        self.model = endpoint.model
        self.max_tokens = max_tokens
        self.pricing = pricing
        self.send_seed = getattr(endpoint, "send_seed", True)

    def complete(self, prompt: str, temperature: float, seed: int) -> dict:
        kwargs = dict(
            model=self.model,
            max_completion_tokens=self.max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        if self.send_seed:
            # best-effort determinism; recorded, never relied on. Some
            # OpenAI-compatible shims (Google AI Studio) reject the field.
            kwargs["seed"] = seed
        resp = self._client.chat.completions.create(**kwargs)
        return normalise_openai_response(resp, overrides=self.pricing)


def make_client(endpoint, pricing=None):
    """Accepts anything endpoint-shaped (ModelEndpoint or SUTConfig)."""
    provider = endpoint.provider
    if provider == "anthropic":
        return AnthropicClient(endpoint, pricing=pricing)
    if provider in ("openai", "openai_compatible"):
        return OpenAICompatibleClient(endpoint, pricing=pricing)
    raise ValueError(f"Unknown provider: {provider}")
