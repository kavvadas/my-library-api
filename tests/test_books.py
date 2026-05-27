import uuid
from tests.conftest import HEADERS, client
import pytest

def unique_isbn():
    return str(uuid.uuid4().int)[:10]

@pytest.fixture
def book_id(client):
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "isbn": unique_isbn(),
        "publication_year": 2020,
        "status": "available"
    }, headers=HEADERS)
    assert response.status_code == 201
    return response.json()["id"]

def test_create_book(client):
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "isbn": unique_isbn(),
        "publication_year": 2020,
        "status": "available"
    }, headers=HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["publication_year"] == 2020
    assert data["status"] == "available"
    assert "id" in data

def test_create_book_invalid_api_key(client):
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "isbn": unique_isbn(),
        "publication_year": 2020,
        "status": "available"
    }, headers={"X-API-Key": "invalid_key"})
    assert response.status_code == 401

def test_get_book(client, book_id):
    response = client.get(f"/books/{book_id}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id

def test_get_non_existent_book(client):
    response = client.get("/books/9999", headers=HEADERS)
    assert response.status_code == 404

def test_get_books_pagination(client):
    for i in range(15):
        client.post("/books/", json={
            "title": f"Test Book {i}",
            "author": "Test Author",
            "isbn": unique_isbn(),
            "publication_year": 2020,
            "status": "available"
        }, headers=HEADERS)
    response = client.get("/books/?page=2&size=10", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

def test_get_books_search_by_title(client):
    client.post("/books/", json={
        "title": "Unique Title",
        "author": "Test Author",
        "isbn": unique_isbn(),
        "publication_year": 2020,
        "status": "available"
    }, headers=HEADERS)
    client.post("/books/", json={
        "title": "Unique Title",
        "author": "Another Author",
        "isbn": unique_isbn(),
        "publication_year": 2020,
        "status": "available"
    }, headers=HEADERS)
    response = client.get("/books/?search=Unique", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Unique Title"

def test_get_books_search_by_author(client):
    client.post("/books/", json={
        "title": "Test Book",
        "author": "Unique Author",
        "isbn": unique_isbn(),
        "publication_year": 2020,
        "status": "available"
    }, headers=HEADERS)
    
    client.post("/books/", json={
        "title": "Another Book",
        "author": "Unique Author",
        "isbn": unique_isbn(),  
        "publication_year": 2020,
        "status": "available"
    }, headers=HEADERS)
    response = client.get("/books/?search=Unique", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["author"] == "Unique Author"

def test_get_books_invalid_pagination(client):
    response = client.get("/books/?page=0&size=10", headers=HEADERS)
    assert response.status_code == 400
    response = client.get("/books/?page=1&size=0", headers=HEADERS)
    assert response.status_code == 400

def test_get_books_no_results(client):
    response = client.get("/books/?search=NoSuchBook", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_get_books_invalid_api_key(client):
    response = client.get("/books/", headers={"X-API-Key": "invalid_key"})
    assert response.status_code == 401

def test_update_book(client, book_id):
    response = client.put(f"/books/{book_id}", json={
        "title": "Updated Title",
        "author": "Updated Author",
        "isbn": unique_isbn(),
        "publication_year": 2021,
        "status": "checked_out"
    }, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"
    assert data["publication_year"] == 2021
    assert data["status"] == "checked_out"

def test_update_non_existent_book(client):
    response = client.put("/books/9999", json={
        "title": "Updated Title",
        "author": "Updated Author",
        "isbn": unique_isbn(),
        "publication_year": 2021,
        "status": "checked_out"
    }, headers=HEADERS)
    assert response.status_code == 404

def test_delete_book(client, book_id):
    response = client.delete(f"/books/{book_id}", headers=HEADERS)
    assert response.status_code == 204
    response = client.get(f"/books/{book_id}", headers=HEADERS)
    assert response.status_code == 404
