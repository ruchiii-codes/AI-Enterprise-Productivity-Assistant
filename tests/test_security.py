import os

from fastapi.testclient import TestClient

from server.main import app


client = TestClient(app)


def test_chat_requires_authentication():
    response = client.post(
        "/chat",
        json={
            "question": "Hello",
        },
    )

    assert response.status_code in (401, 403)


def test_jwt_secret_is_loaded_from_environment():
    assert os.getenv("JWT_SECRET_KEY")