from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


def test_experiment_assignment():
    response = client.post(
        "/experiment/assign",
        json={
            "user_id": "user_123",
            "experiment_name": "homepage-ranking-test"
        }
    )
    assert response.status_code == 200
    assert "experiment_group" in response.json()