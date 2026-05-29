from tests.conftest import client


def test_invalid_api_key(client):
    response = client.get("/books/", headers={"X-API-Key": "invalid_key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API Key"}

def test_missing_api_key(client):
    response = client.get("/books/")
    assert response.status_code == 422  
    assert "detail" in response.json()

def test_valid_api_key(client):
    response = client.get("/books/", headers={"X-API-Key": "test_api_key"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)



