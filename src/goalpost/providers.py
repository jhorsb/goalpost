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


def compute_cost(model: str, *, input_tokens: int, output_tokens: int) -> float:
    rates = PRICING.get(model, _DEFAULT_PRICING)
    return (
        input_tokens / 1e6 * rates["input"]
        + output_tokens / 1e6 * rates["output"]
    )


def normalise_anthropic_response(resp) -> dict:
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
        "cost_usd": compute_cost(resp.model, **usage),
        "model_fingerprint": resp.model,
        "stop_reason": resp.stop_reason,
    }


def normalise_openai_response(resp) -> dict:
    choice = resp.choices[0]
    usage = {
        "input_tokens": resp.usage.prompt_tokens,
        "output_tokens": resp.usage.completion_tokens,
    }
    return {
        "text": choice.message.content or "",
        "usage": usage,
        "cost_usd": compute_cost(resp.model, **usage),
        "model_fingerprint": getattr(resp, "system_fingerprint", None) or resp.model,
        "stop_reason": choice.finish_reason,
    }


class AnthropicClient:
    """Live client. Constructed lazily so offline tests never import creds."""

    def __init__(self, model: str, max_tokens: int = 2048):
        import anthropic

        self._client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens

    def complete(self, prompt: str, temperature: float, seed: int) -> dict:
        # The Messages API has no sampling-seed parameter; the derived seed
        # is recorded in the transcript for provenance but cannot be passed.
        resp = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return normalise_anthropic_response(resp)


class OpenAIClient:
    def __init__(self, model: str, max_tokens: int = 2048):
        import openai

        self._client = openai.OpenAI()
        self.model = model
        self.max_tokens = max_tokens

    def complete(self, prompt: str, temperature: float, seed: int) -> dict:
        resp = self._client.chat.completions.create(
            model=self.model,
            max_completion_tokens=self.max_tokens,
            temperature=temperature,
            seed=seed,  # best-effort determinism; recorded, never relied on
            messages=[{"role": "user", "content": prompt}],
        )
        return normalise_openai_response(resp)


def make_client(provider: str, model: str):
    if provider == "anthropic":
        return AnthropicClient(model)
    if provider == "openai":
        return OpenAIClient(model)
    raise ValueError(f"Unknown provider: {provider}")


def api_key_present(provider: str) -> bool:
    env = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}
    return bool(os.environ.get(env.get(provider, "")))
