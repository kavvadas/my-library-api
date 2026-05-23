import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import SessionLocal
from app.main import app

HEADERS = {
    "X-API-Key": "test_api_key"
}


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_db(db_session):
    db_session.execute(text("TRUNCATE TABLE books RESTART IDENTITY CASCADE"))
    db_session.commit()
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c