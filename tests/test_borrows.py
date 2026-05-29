from tests.conftest import client

def test_borrow_book(client,auth_headers,test_book):
    response = client.post(
        f"/borrow/{test_book.id}",
        headers=auth_headers
    )

    assert response.status_code == 201

    data = response.json()
    assert data["book"]["id"] == test_book.id

def test_borrow_requires_auth(client,test_book):
    response = client.post(
        f"/borrow/{test_book.id}"
    )

    assert response.status_code == 401

def test_borrow_unavailable_book(
    client,
    auth_headers,
    test_book
):
    # First borrow
    client.post(
        f"/borrow/{test_book.id}",
        headers=auth_headers
    )

    # Second borrow attempt
    response = client.post(
        f"/borrow/{test_book.id}",
        headers=auth_headers
    )

    assert response.status_code == 400




def test_return_book(
    client,
    auth_headers,
    test_book
):
    borrow_response = client.post(
        f"/borrow/{test_book.id}",
        headers=auth_headers
    )

    borrow_id = borrow_response.json()["id"]

    response = client.post(
        f"/borrow/{borrow_id}/return",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["return_date"] is not None


def test_return_book_twice(
    client,
    auth_headers,
    test_book
):
    borrow_response = client.post(
        f"/borrow/{test_book.id}",
        headers=auth_headers
    )

    borrow_id = borrow_response.json()["id"]

    client.post(
        f"/borrow/{borrow_id}/return",
        headers=auth_headers
    )

    response = client.post(
        f"/borrow/{borrow_id}/return",
        headers=auth_headers
    )

    assert response.status_code == 400


def test_return_nonexistent_borrow(
    client,
    auth_headers
):
    response = client.post(
        "/borrow/999/return",
        headers=auth_headers
    )

    assert response.status_code == 404