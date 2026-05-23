# My Library API

REST API for library book management using FastAPI and PostgreSQL.

## Features

- CRUD operations for books
- Search by title or author
- Pagination (1-10 books per page)
- API Key authentication
- Docker support
- PostgreSQL integration
- Pytest tests

---

## Setup

Create `.env` file:

```env
DATABASE_URL = "postgresql://postgres:postgres@db:5432/library_db"
API_KEY = "test_api_key"
```

Run:

```bash
docker compose up --build
```

API runs at:

```txt
http://localhost:8000
```

Swagger docs:

```txt
http://localhost:8000/docs
```

---

## Authentication

Add header:

```txt
X-API-Key: test_api_key
```

---

## Run tests

```bash
docker compose run --rm test 
```

---

## Example request 

```bash
curl -X POST "http://localhost:8000/books/" \
-H "Content-Type: application/json" \
-H "X-API-Key: test_api_key" \
-d '{
    "title": "Σπουδή Στο Κόκκινο",
    "author": "Conan Doyle",
    "isbn": "123456789",
    "publication_year": 1887,
    "status": "available"
}'
```

