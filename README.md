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
## Improvements and new features (v0.2.0)

- User management using JWT token authorization and argon2
- Borrow book logic system

---

### Done 

* login endpoints
* token creation JWT
* password hashin (argon2)
* install dependencies
* apply current_user to borrow router

---

## Setup

Create `.env` file:

```env
DATABASE_URL = "postgresql://postgres:postgres@db:5432/library_db"
API_KEY = "test_api_key"
VERSION = "v0.2.0"
```

Run:

```bash
docker compose up --build
```
**This will also run the tests.**

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

## Example requests for books

*Create book example:*
```bash
curl -X 'POST' \
  'http://localhost:8000/books/' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Σπουδή Στο Κόκκινο",
    "author": "Conan Doyle",
    "isbn": "123456789",
    "publication_year": 1887
}'
```

*Get books example:*
```bash
curl -X 'GET' \
  'http://localhost:8000/books/?page=1&size=10' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key'
```

*Search books by title exapmle:*
**requirement**: a book's title contains = "Σπουδ"
```bash
curl -X 'GET' \
  'http://localhost:8000/books/?page=1&size=10&search=%CE%A3%CF%80%CE%BF%CF%85%CE%B4' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key'
```

*Get book by id example:* 
**requirement**: a book exists with id=2
```bash
curl -X 'GET' \
  'http://localhost:8000/books/2' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key'
```

---

## Example requests for users

*Create user example:*
```bash
curl -X 'POST' \
  'http://localhost:8000/user/' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "Dimitris Kavvadas",
  "email": "example@email.com",
  "password": "example_password"
}'
```

*Get users example:*
```bash
curl -X 'GET' \
  'http://localhost:8000/user/?page=1&size=10' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key'
```

*Get user by id example:*
**requirement**: a user exists with id=1
```bash
curl -X 'GET' \
  'http://localhost:8000/user/1' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key'
```

*Get users by role example(user):*
```bash
curl -X 'GET' \
  'http://localhost:8000/user/role/user' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key'
```

---

## Example requests for borrows

*Borrow book example:*
**requirements**: 
* a user exists with id=1
* a book exists with id=2  
```bash
curl -X 'POST' \
  'http://localhost:8000/borrow/2?user_id=1' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key' \
  -d ''
```

*Return a book example:*
**requirements**: a borrowing record exists with id=1
```bash
curl -X 'POST' \
  'http://localhost:8000/borrow/1/return' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key' \
  -d ''
```

*Get borrowing records:*
```bash
curl -X 'GET' \
  'http://localhost:8000/borrow/' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key'
```

*Get borrowing records by user_id:*
**requiremenets**: a user exists with id=1
```bash
curl -X 'GET' \
  'http://localhost:8000/borrow/user/1' \
  -H 'accept: application/json' \
  -H 'x-api-key: test_api_key'
```