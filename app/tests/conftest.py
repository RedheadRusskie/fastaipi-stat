import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.dependencies import get_db
from unittest.mock import MagicMock, patch
from app.db.base import Base


class MockSession:
    def __init__(self, existing_user=None):
        self.existing_user = existing_user
        self.added = []
        self.committed = False
        self.refreshed = []

    def query(self, model):
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = self.existing_user

        return mock_query

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        self.refreshed.append(obj)


@pytest.fixture
def mock_get_db():
    yield MockSession()


@pytest.fixture(autouse=True)
def patch_pwd_context_hash():
    with patch("app.auth.pwd_context.hash", side_effect=lambda x: f"hashed-{x[:72]}"):
        yield


@pytest.fixture(autouse=True)
def patch_create_all():
    with patch.object(Base.metadata, "create_all", lambda bind: None):
        yield


@pytest.fixture
def client(mock_get_db):
    app.dependency_overrides[get_db] = lambda: mock_get_db
    return TestClient(app)
