from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi import _rate_limit_exceeded_handler


def test_rate_limit_returns_429():
    app = FastAPI()

    limiter = Limiter(key_func=get_remote_address)

    app.state.limiter = limiter
    app.add_exception_handler(
        RateLimitExceeded,
        _rate_limit_exceeded_handler,
    )
    app.add_middleware(SlowAPIMiddleware)

    @app.get("/test")
    @limiter.limit("2/minute")
    def test_endpoint(request: Request):
        return {"status": "ok"}

    client = TestClient(app)

    assert client.get("/test").status_code == 200
    assert client.get("/test").status_code == 200
    assert client.get("/test").status_code == 429