from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import _or_


from app.database import get_db
from app.dependencies import verify_api_key
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookResponse


router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(verify_api_key)]
)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    book = Book(**book.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.get("/", response_model=list[BookResponse])
def get_books(page: int = 1, size: int = 10, search: str | None = None, db: Session = Depends(get_db)):
    if page < 1 or size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page and size must be positive integers")
    query = db.query(Book).order_by(Book.id)
    if search:
        query = query.filter(_or_(
            Book.title.ilike(f"%{search}%"),
            Book.author.ilike(f"%{search}%")
        ))
    books = query.offset((page - 1) * size).limit(size).all()
    return books

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    for key, value in book_update.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(book)
    db.commit()
    return None
