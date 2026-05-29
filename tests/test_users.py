from tests.conftest import HEADERS,auth_headers

def test_create_user(client):
    response = client.post(
        "/user/",
        json = {
            "username" : "test_user",
            "email" : "test_email@email.com",
            "password" : "test_password2"
        },
        headers=HEADERS
    )

    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "test_user"
    assert data["email"] == "test_email@email.com"

def test_duplicate_user(client):

    client.post(
        "/user/",
        json = {
            "username" : "dimitris",
            "email" : "test2_email@email.com",
            "password" : "test_password3"
        },
        headers=HEADERS
    )

    response = client.post(
        "/user/",
        json = {
            "username" : "dimitris",
            "email" : "test3_email@email.com",
            "password" : "test_password3"
        },
        headers=HEADERS
    )

    assert response.status_code == 400



def test_get_me(client, auth_headers):
    response = client.get(
        "/user/me",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "dimitris"
    


def test_get_all_users(
    client,
    auth_headers,
    test_user
):
    response = client.get(
        "/user/",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1


def test_get_user_by_id(
    client,
    auth_headers,
    test_user
):
    response = client.get(
        f"/user/{test_user.id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == test_user.id
    assert data["username"] == test_user.username


def test_get_user_not_found(
    client,
    auth_headers
):
    response = client.get(
        "/user/999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_get_my_borrows_empty(
    client,
    auth_headers
):
    response = client.get(
        "/user/me/borrows",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []