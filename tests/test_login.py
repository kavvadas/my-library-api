from tests.conftest import HEADERS

def test_login_success(client,test_user):
    response = client.post(
        "/auth/login",
        data = {
            "username":"dimitris",
            "password":"test_password"
        },
        headers=HEADERS
    )

    assert response.status_code==202

    data = response.json()

    assert "access_token" in data
    assert data["token_type"]=="bearer"


def test_login_invalid_password(client,test_user):
    response = client.post(
        "/auth/login",
        data = {
            "username" : "dimitris",
            "password" : "wrong_password"
        },
        headers= HEADERS
    )

    assert response.status_code == 401

def test_login_invalid_user(client, test_user):
    response = client.post(
        "/auth/login",
        data = {
            "username" : "wrong_username",
            "password":"test_password"
        },
        headers=HEADERS
    )

    assert response.status_code == 401