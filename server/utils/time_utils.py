"""Time helpers.

``datetime.utcnow()`` is deprecated and scheduled for removal, but its
documented replacement -- ``datetime.now(timezone.utc)`` -- returns an *aware*
datetime, and every ``DateTime`` column in this project is naive (none declare
``timezone=True``). Mixing the two raises ``TypeError: can't compare
offset-naive and offset-aware datetimes`` on expiry checks such as the
verification and password-reset comparisons.

Stripping the tzinfo keeps the stored values byte-identical to what
``utcnow()`` produced, so no migration or data change is required. If the
columns ever move to ``DateTime(timezone=True)`` -- worth doing on Postgres,
which has a real timestamptz -- this helper is the single place to change.
"""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Current UTC time as a naive datetime, matching the naive columns."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
