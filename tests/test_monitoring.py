from fastapi.testclient import TestClient

from server.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "running"
    }


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "AI Enterprise Productivity Assistant" in response.json()["message"]