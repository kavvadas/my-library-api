import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.models import User, Book
from app.utils.security import hash_password, create_access_token

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
    db_session.execute(
        text("TRUNCATE TABLE books,users,borrow_records RESTART IDENTITY CASCADE")
    )
    db_session.commit()
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user(db_session):
    user = User(
        username="dimitris",
        email="kabbadasd@gmail.com",
        hashed_password=hash_password("test_password")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(
        data = {
            "sub":str(test_user.id),
            "role":test_user.role
        }
    )
    return {
        "Authorization" : f"Bearer {token}",
        "X-Api-Key" : "test_api_key"
    }

@pytest.fixture
def test_book(db_session):
    book = Book(
        title="Σπουδή στο Ρόζ",
        author="Dr. Watson",
        isbn="9780132350884",
        publication_year=2008
    )

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    return book