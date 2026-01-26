from uuid import uuid4
from app.models import User
from app.auth import get_current_user


def test_post_dataset_success(client, mock_get_db, app_fixture):
    user = {"id": "1234", "username": "johndoe"}
    dataset = {"name": "My Dataset", "description": "Test dataset"}

    mock_get_db.existing_user = User(id=user["id"], username=user["username"])

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user["id"]}

    response = client.post("/dataset", json=dataset)

    assert response.status_code == 200
    assert response.json()["message"] == "Dataset My Dataset created successfully"
    assert "dataset_id" in response.json()

    app_fixture.dependency_overrides.clear()


def test_post_dataset_user_not_found(client, mock_get_db, app_fixture):
    user = {"id": "1234", "username": "johndoe"}
    dataset_payload = {"name": "Ghost Dataset", "description": "No user exists"}

    mock_get_db.existing_user = None

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user["id"]}

    response = client.post("/dataset", json=dataset_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Could not find user by specified user ID"

    app_fixture.dependency_overrides.clear()


def test_get_dataset_single(client, mock_get_db, app_fixture):
    user = {"id": "1234", "username": "johndoe"}
    dataset_id = str(uuid4())

    mock_get_db.existing_user = {"id": user["id"], "username": user["username"]}
    mock_get_db.existing_dataset = {
        "id": dataset_id,
        "name": "Dataset One",
        "user_id": user["id"],
        "description": "Test",
        "created_at": "2026-01-22T12:00:00",
    }

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user["id"]}

    response = client.get(f"/dataset?dataset_id={dataset_id}")

    assert response.status_code == 200
    assert response.json()["id"] == dataset_id
    assert response.json()["name"] == "Dataset One"

    app_fixture.dependency_overrides.clear()


def test_get_dataset_list(client, mock_get_db, app_fixture):
    user = {"id": "1234", "username": "johndoe"}

    mock_get_db.existing_user = {"id": user["id"], "username": user["username"]}
    mock_get_db.existing_datasets = [
        {
            "id": str(uuid4()),
            "name": f"Dataset {i}",
            "user_id": user["id"],
            "description": f"Desc {i}",
            "created_at": "2026-01-22T12:00:00",
        }
        for i in range(3)
    ]

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user["id"]}

    response = client.get("/dataset")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == "Dataset 0"

    app_fixture.dependency_overrides.clear()


def test_delete_dataset_success(client, mock_get_db, app_fixture):
    user = {"id": "1234", "username": "johndoe"}
    dataset_id = str(uuid4())

    mock_get_db.existing_user = {"id": user["id"], "username": user["username"]}
    mock_get_db.existing_dataset = {"id": dataset_id, "user_id": user["id"]}

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user["id"]}

    response = client.delete(f"/dataset/{dataset_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Dataset of ID removed successfully"
    assert response.json()["dataset_id"] == dataset_id

    app_fixture.dependency_overrides.clear()


def test_delete_dataset_not_found(client, mock_get_db, app_fixture):
    user = {"id": "1234", "username": "johndoe"}
    dataset_id = str(uuid4())

    mock_get_db.existing_user = {"id": user["id"], "username": user["username"]}
    mock_get_db.existing_dataset = None

    app_fixture.dependency_overrides[get_current_user] = lambda: {"user_id": user["id"]}

    response = client.delete(f"/dataset/{dataset_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Could not find dataset with supplied ID"

    app_fixture.dependency_overrides.clear()
