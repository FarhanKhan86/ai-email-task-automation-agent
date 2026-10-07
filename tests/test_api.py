from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agent_run():
    response = client.post(
        "/api/agent/run",
        json={
            "request": "Draft an email to hiring@example.com about my interview and remind me tomorrow."
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["completed"] == 2
    assert data["summary"]["failed"] == 0
