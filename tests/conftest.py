"""Shared pytest configuration.

`server.config.Settings` requires OPENROUTER_API_KEY and JWT_SECRET_KEY, and
several modules read configuration at import time. Tests must not depend on a
developer's real `.env`, so placeholder values are installed here before any
`server.*` module is imported.

Real environment values still win: these are only applied when the variable is
absent, so running the suite locally with a populated `.env` behaves as before.
"""

import os

import pytest

_TEST_DEFAULTS = {
    "OPENROUTER_API_KEY": "test-openrouter-key",
    "JWT_SECRET_KEY": "test-jwt-secret-not-for-production",
}

for _key, _value in _TEST_DEFAULTS.items():
    os.environ.setdefault(_key, _value)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Give every test a fresh rate-limit budget.

    slowapi keys limits by client address, and the TestClient always presents
    the same one. Without this, requests made by one test count against the
    limits of the next -- several auth tests register more users than the
    5/minute limit allows.
    """
    from server.utils.rate_limiter import limiter

    limiter.reset()

    yield

    limiter.reset()
