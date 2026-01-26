from uuid import uuid4
from datetime import datetime
from app.models import User, Dataset, DatasetRow
from app.auth import get_current_user


def test_create_row_success(client, mock_get_db, app_fixture):
    user = User(id="1234", username="johndoe", hashed_password="hashed")
    dataset = Dataset(id=str(uuid4()), user_id=user.id, name="Test", description="Desc")

    mock_get_db.existing_user = user
    mock_get_db.existing_dataset = dataset

    payload = [{"dataset_id": dataset.id, "data": {"col1": 42}}]

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user.id}

    response = client.post("/row", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Created 1 entries successfully"
    assert len(data["entries"]) == 1
    assert data["entries"][0]["dataset_id"] == dataset.id

    app_fixture.dependency_overrides.clear()


def test_create_row_user_not_found(client, mock_get_db, app_fixture):
    mock_get_db.existing_user = None
    dataset_id = str(uuid4())

    payload = [{"dataset_id": dataset_id, "data": {"col1": 42}}]

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": "mock-id"}

    response = client.post("/row", json=payload)
    assert response.status_code == 404
    assert "Could not find user" in response.json()["detail"]

    app_fixture.dependency_overrides.clear()


def test_read_rows_success(client, mock_get_db, app_fixture):
    user = User(id="1234", username="johndoe", hashed_password="hashed")
    dataset = Dataset(id=str(uuid4()), user_id=user.id, name="Test", description="Desc")
    row = DatasetRow(
        id=str(uuid4()),
        dataset_id=dataset.id,
        data={"col1": 10},
        created_at=datetime.now(),
    )

    mock_get_db.existing_user = user
    mock_get_db.existing_dataset = dataset
    mock_get_db.existing_dataset_rows = [row]

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user.id}

    response = client.get(f"/row/{dataset.id}")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["dataset_id"] == dataset.id

    app_fixture.dependency_overrides.clear()


def test_delete_row_success(client, mock_get_db, app_fixture):
    user = User(id="1234", username="johndoe", hashed_password="hashed")
    dataset = Dataset(id=str(uuid4()), user_id=user.id, name="Test", description="Desc")
    row = DatasetRow(
        id=str(uuid4()),
        dataset_id=dataset.id,
        data={"col1": 10},
        created_at=datetime.now(),
    )

    mock_get_db.existing_user = user
    mock_get_db.existing_row = row
    mock_get_db.existing_dataset = dataset

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user.id}

    response = client.delete(f"/row/{row.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Row deleted successfully"
    assert data["row_id"] == str(row.id)

    app_fixture.dependency_overrides.clear()
