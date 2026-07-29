"""Small retry helper with exponential backoff and jitter."""

import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry_call(
    fn: Callable[[], T],
    *,
    attempts: int = 4,
    base_delay: float = 0.5,
    retryable: tuple[type[BaseException], ...] = (),
    sleeper: Callable[[float], object] = time.sleep,
    jitter: Callable[[], float] | None = None,
) -> T:
    """Call ``fn``, retrying selected exceptions with exponential backoff."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    jitter = jitter or (lambda: random.uniform(0, base_delay / 2))
    for attempt in range(attempts):
        try:
            return fn()
        except retryable:
            if attempt == attempts - 1:
                raise
            sleeper(base_delay * 2**attempt + jitter())

    raise RuntimeError("retry loop exhausted without returning or raising")
