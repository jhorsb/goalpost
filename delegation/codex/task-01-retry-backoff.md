# Codex task 01 — retry/backoff for provider clients

## Context (all you need)
Goalpost is a Python 3.12 CLI that audits LLM screening pipelines by making
repeated API calls through thin provider clients in `src/goalpost/providers.py`
(`AnthropicClient`, `OpenAICompatibleClient`). Transient provider failures
(rate limits, 5xx, timeouts) currently kill an audit run. Add a small,
dependency-free retry helper and wire both clients through it.

## Interface contract
New module `src/goalpost/retry.py`:

```python
def retry_call(
    fn,                       # zero-arg callable
    *,
    attempts: int = 4,        # total attempts, >= 1
    base_delay: float = 0.5,  # seconds; delay_i = base_delay * 2**i + jitter()
    retryable: tuple[type[BaseException], ...] = (),
    sleeper=time.sleep,       # injected for tests
    jitter=None,              # zero-arg -> float; default: random.uniform(0, base_delay/2)
):
    """Call fn; on a retryable exception sleep and retry with exponential
    backoff + jitter; re-raise after the final attempt. Non-retryable
    exceptions propagate immediately."""
```

Wire-up in `src/goalpost/providers.py`: both clients' `.complete` must route
the SDK call through `goalpost.retry.retry_call` (imported as
`from goalpost import retry` / called as `retry.retry_call(...)` so the test
monkeypatch on `goalpost.retry.retry_call` takes effect), with `attempts>=3`
and provider-appropriate `retryable` classes:
- OpenAI: `openai.RateLimitError`, `openai.APIConnectionError`, `openai.APITimeoutError`, `openai.InternalServerError`
- Anthropic: `anthropic.RateLimitError`, `anthropic.APIConnectionError`, `anthropic.APITimeoutError`, `anthropic.InternalServerError`

## Failing tests (already committed — your job is GREEN)
`tests/codex/test_task01_retry.py` — run: `uv run pytest -m codex tests/codex/test_task01_retry.py`

## File-touch allowlist
- `src/goalpost/retry.py` (new)
- `src/goalpost/providers.py` (wire-up only; do not change pricing,
  normalisation functions, or client constructor signatures)

## Constraints
- No new dependencies. No network in tests. Match repo style (typed, tested).
- Do not modify any test file.
- Do not add retries anywhere else (runner has its own budget semantics).

## Definition of done
- `uv run pytest -m codex tests/codex/test_task01_retry.py` green
- `uv run pytest` (default suite) green
- Nothing else in the diff

## Branch
`codex/task-01-retry-backoff`

## Return format
Short summary of approach + anything you could not satisfy and why.
