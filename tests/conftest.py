"""Shared pytest configuration.

`server.config.Settings` requires OPENROUTER_API_KEY and JWT_SECRET_KEY, and
several modules read configuration at import time. Tests must not depend on a
developer's real `.env`, so placeholder values are installed here before any
`server.*` module is imported.

Real environment values still win: these are only applied when the variable is
absent, so running the suite locally with a populated `.env` behaves as before.
"""

import os

_TEST_DEFAULTS = {
    "OPENROUTER_API_KEY": "test-openrouter-key",
    "JWT_SECRET_KEY": "test-jwt-secret-not-for-production",
}

for _key, _value in _TEST_DEFAULTS.items():
    os.environ.setdefault(_key, _value)
