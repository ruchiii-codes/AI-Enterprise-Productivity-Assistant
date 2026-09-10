from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from server.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "running",
        "database": "ok",
    }


def test_health_endpoint_reports_unreachable_database():
    """A load balancer must be able to tell a broken instance from a live one.

    Without this, /health answers 200 on process liveness alone and traffic
    keeps arriving at an instance that cannot serve a single request.
    """
    failure = OperationalError("SELECT 1", {}, Exception("connection refused"))

    with patch("server.main.engine.connect", side_effect=failure):
        response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {
        "status": "degraded",
        "database": "unreachable",
    }


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "AI Enterprise Productivity Assistant" in response.json()["message"]
