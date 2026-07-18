"""RED tests for delegation/codex/task-01-retry-backoff.md.
Run with: pytest -m codex tests/codex/test_task01_retry.py"""

import pytest

pytestmark = pytest.mark.codex


class Transient(Exception):
    pass


class Permanent(Exception):
    pass


def make_flaky(fail_times, exc=Transient):
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] <= fail_times:
            raise exc("boom")
        return "ok"

    fn.calls = calls
    return fn


def test_retries_transient_and_succeeds():
    from goalpost.retry import retry_call

    sleeps = []
    fn = make_flaky(2)
    result = retry_call(
        fn, attempts=4, base_delay=0.5, retryable=(Transient,),
        sleeper=sleeps.append, jitter=lambda: 0.0,
    )
    assert result == "ok"
    assert fn.calls["n"] == 3
    assert sleeps == [0.5, 1.0]  # exponential, no jitter


def test_jitter_added_to_delays():
    from goalpost.retry import retry_call

    sleeps = []
    retry_call(
        make_flaky(1), attempts=3, base_delay=1.0, retryable=(Transient,),
        sleeper=sleeps.append, jitter=lambda: 0.25,
    )
    assert sleeps == [1.25]


def test_permanent_errors_never_retried():
    from goalpost.retry import retry_call

    fn = make_flaky(5, exc=Permanent)
    with pytest.raises(Permanent):
        retry_call(fn, attempts=4, base_delay=0.1, retryable=(Transient,),
                   sleeper=lambda s: None)
    assert fn.calls["n"] == 1


def test_gives_up_after_attempts_and_reraises():
    from goalpost.retry import retry_call

    fn = make_flaky(99)
    with pytest.raises(Transient):
        retry_call(fn, attempts=3, base_delay=0.1, retryable=(Transient,),
                   sleeper=lambda s: None)
    assert fn.calls["n"] == 3


def test_provider_clients_wrap_completions_with_retry(monkeypatch):
    """Both live clients must route .complete through retry_call with
    provider-appropriate retryable exception classes."""
    import goalpost.providers as providers

    seen = {}

    def fake_retry_call(fn, **kwargs):
        seen.update(kwargs)
        return {"text": "", "usage": {"input_tokens": 0, "output_tokens": 0},
                "cost_usd": 0.0, "model_fingerprint": "f", "stop_reason": "stop"}

    monkeypatch.setattr("goalpost.retry.retry_call", fake_retry_call)
    from goalpost.config import ModelEndpoint

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    client = providers.make_client(
        ModelEndpoint(provider="openai", model="gpt-4o-mini-2024-07-18")
    )
    client.complete(prompt="p", temperature=0.0, seed=1)
    assert seen.get("attempts", 0) >= 3
    assert seen.get("retryable")
