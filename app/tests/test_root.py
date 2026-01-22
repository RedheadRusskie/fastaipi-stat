import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_read_root(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI + Postgres are live"}
