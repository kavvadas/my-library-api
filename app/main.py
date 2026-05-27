from fastapi import FastAPI

from app.database import engine, Base
from app.routers.books import router as books_router
from app.routers.borrow import router as borrow_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router

import time
from sqlalchemy.exc import OperationalError

def wait_for_db(engine):
    for _ in range(10):
        try:
            with engine.connect():
                return
        except OperationalError:
            time.sleep(1)
    raise Exception("DB not ready")

app = FastAPI(
    title="My-Library-API",
    version="0.2.0"
)


@app.on_event("startup")
def on_startup():
    wait_for_db(engine)
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to My Library API!"}

app.include_router(books_router)
app.include_router(borrow_router)
app.include_router(users_router)
app.include_router(auth_router)