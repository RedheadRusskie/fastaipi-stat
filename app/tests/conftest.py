import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.dependencies import get_db
from unittest.mock import MagicMock, patch
from app.db.base import Base
from uuid import uuid4
from datetime import datetime, timezone


class MockSession:
    def __init__(self):
        self.existing_user = None
        self.existing_dataset = None
        self.existing_datasets = []
        self.existing_dataset_rows = []
        self.existing_row = None
        self.added = []
        self.deleted = None
        self.committed = False
        self.refreshed = []

    def query(self, model):
        mock_query = MagicMock()

        if model.__name__ == "User":
            mock_query.filter.return_value.first.return_value = self.existing_user

        elif model.__name__ == "Dataset":
            mock_query.filter.return_value.first.return_value = self.existing_dataset
            mock_query.filter.return_value.all.return_value = self.existing_datasets

        elif model.__name__ == "DatasetRow":

            def first():
                if self.existing_row is not None:
                    return self.existing_row

                if self.existing_dataset_rows:
                    return self.existing_dataset_rows[0]

                return None

            mock_query.filter.return_value.first.side_effect = first
            mock_query.filter.return_value.all.return_value = self.existing_dataset_rows
            mock_query.filter.return_value.offset.return_value.limit.return_value.all.return_value = (
                self.existing_dataset_rows
            )

        return mock_query

    def _ensure_defaults(self, obj):
        if getattr(obj, "id", None) is None:
            obj.id = uuid4()

        if getattr(obj, "created_at", None) is None:
            obj.created_at = datetime.now(timezone.utc)

    def add(self, obj):
        self._ensure_defaults(obj)
        self.added.append(obj)

    def add_all(self, objs):
        for obj in objs:
            self._ensure_defaults(obj)
            self.added.append(obj)

    def delete(self, obj):
        self.deleted = obj

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        self._ensure_defaults(obj)
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
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def app_fixture():
    yield app
