"""Request rate limiting.

Two things have to be right for limits to mean anything in a deployment with
more than one worker or instance:

1. **The key must identify the client.** slowapi's ``get_remote_address``
   reads the socket peer, which behind a load balancer is the balancer itself.
   Every user would then share a single bucket, so one noisy client would lock
   out everybody -- rate limiting as a self-inflicted outage. Behind a proxy
   the real address comes from X-Forwarded-For instead.

2. **The store must be shared.** The default in-memory store is per worker
   process, so the configured limits are silently multiplied by workers times
   instances. Redis makes one budget span the deployment.
"""

import logging
from typing import Optional

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from server.config import settings

logger = logging.getLogger(__name__)


def client_identifier(request: Request) -> str:
    """The address to rate-limit on.

    X-Forwarded-For is appended to by each hop, so the entry this app should
    trust is counted from the right: with one proxy the client is the last
    entry, with two it is the second to last. Anything further left was
    supplied by the client and can be forged.

    TRUSTED_PROXY_COUNT defaults to 0, so the header is ignored unless a
    deployment declares its proxies. Trusting it unconditionally would let any
    caller pick their own bucket and bypass every limit.
    """
    proxy_count = settings.TRUSTED_PROXY_COUNT

    if proxy_count > 0:
        forwarded = request.headers.get("X-Forwarded-For")

        if forwarded:
            hops = [hop.strip() for hop in forwarded.split(",") if hop.strip()]

            if len(hops) >= proxy_count:
                return hops[-proxy_count]

            # Fewer hops than expected: the request did not arrive through the
            # declared chain, so fall through to the socket address rather
            # than trusting a header that does not match the topology.
            logger.warning(
                "X-Forwarded-For has %d entries but TRUSTED_PROXY_COUNT is %d; "
                "falling back to the peer address.",
                len(hops),
                proxy_count,
            )

    return get_remote_address(request)


def _storage_uri() -> Optional[str]:
    if settings.REDIS_URL:
        logger.info("Rate limiting is using shared Redis storage.")
        return settings.REDIS_URL

    logger.info(
        "Rate limiting is using in-memory storage: limits apply per worker "
        "process. Set REDIS_URL when running more than one."
    )
    return None


limiter = Limiter(
    key_func=client_identifier,
    storage_uri=_storage_uri(),
    # Without this, an unreachable Redis makes every rate-limited route return
    # 500 -- login, register, password reset and /chat all fail, so a cache
    # blip becomes a total outage. The fallback degrades to per-process
    # in-memory limits instead: weaker than shared limits, but the endpoints
    # stay up and stay limited.
    in_memory_fallback_enabled=True,
)
