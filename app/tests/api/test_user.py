from app.models.user import User


def test_register_user_success(client):
    mock_user = {
        "username": "johndoe",
        "password": "password",
    }
    response = client.post("/user", json=mock_user)

    assert response.status_code == 200

    json_data = response.json()

    assert json_data["message"] == f"User {mock_user['username']} created successfully"
    assert "user_id" in json_data


def test_register_user_already_exists(client, mock_get_db):
    mock_user = {
        "id": "1234",
        "username": "johndoe",
        "password": "password",
        "hashed_password": "hashed-password",
    }

    mock_get_db.existing_user = User(
        id=mock_user["id"],
        username=mock_user["username"],
        hashed_password=mock_user["hashed_password"],
    )

    response = client.post(
        "/user",
        json={
            "username": mock_user["username"],
            "password": mock_user["password"],
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User with specified username already exists"
