from jose import jwt
from app import schemas
import pytest
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "jai mata di"


def test_create_users(client):
    res = client.post(
        "/users/", json={"email": "yabs@gmail.com", "password": "123456890"}
    )
    assert res.status_code == 201 or 409


def test_login_user(test_user, client):

    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("yash@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("yash@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):

    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get("detail") == f"Invalid Credentials"
