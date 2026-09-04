from .database import session, client

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'jai mata di'

def test_create_users(client):
    res = client.post(
        "/users/", json={"email": "yabs@gmail.com", "password": "1234567890"} 
    )
    assert res.status_code == 201 or 409
