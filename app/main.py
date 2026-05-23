from fastapi import FastAPI

from app.database import engine, Base
from app.routers.books import router as books_router


Base.metadata.create_all(bind=engine)
app = FastAPI(title="My-Library-API")

@app.get("/")
def root():
    return {"message": "Welcome to My Library API!"}

app.include_router(books_router)

