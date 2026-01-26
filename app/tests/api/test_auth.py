from app.models.user import User
from unittest.mock import patch


def test_login_success(client, mock_get_db):
    user = {
        "id": "1234",
        "username": "johndoe",
        "password": "password",
        "hashed_password": "hashed-password",
        "access_token": "mock-jwt-token",
    }

    mock_get_db.existing_user = User(
        id=user["id"],
        username=user["username"],
        hashed_password=user["hashed_password"],
    )

    with patch("app.api.auth.verify_password", return_value=True), patch(
        "app.api.auth.create_access_token", return_value=user["access_token"]
    ):
        response = client.post(
            "/token",
            data={
                "username": user["username"],
                "password": user["password"],
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": user["access_token"],
        "token_type": "bearer",
    }


def test_login_incorrect_credentials(client, mock_get_db):
    user = {
        "username": "johndoe",
        "password": "wrong-password",
        "hashed_password": "hashed-password",
    }

    mock_get_db.existing_user = User(
        id="1234",
        username=user["username"],
        hashed_password=user["hashed_password"],
    )

    with patch("app.api.auth.verify_password", return_value=False):
        response = client.post(
            "/token",
            data={
                "username": user["username"],
                "password": user["password"],
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"
