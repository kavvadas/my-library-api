from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import verify_api_key
from app.models import Book, BorrowRecord, BookStatus
from app.schemas import BorrowRecordResponse
from datetime import datetime,timezone
router = APIRouter(
    prefix="/borrow",
    tags=["borrow"],
    dependencies=[Depends(verify_api_key)])

@router.post("/{book_id}",response_model=BorrowRecordResponse, status_code=status.HTTP_201_CREATED)
def borrow_book(book_id: int,user_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.status == BookStatus.checked_out:
        raise HTTPException(status_code=400, detail = "Book is already borrowed")
    

    active = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.book_id == book_id,
        BorrowRecord.return_date.is_(None)
    ).first()

    if active:
        raise HTTPException(
            status_code=400,
            detail="You already borrowed this book"
        )
    
    borrow = BorrowRecord(
        user_id = user_id,
        book_id = book_id,
        borrow_date = datetime.now(timezone.utc),
        return_date = None
    )

    book.status = BookStatus.checked_out
    db.add(borrow)
    db.commit()
    db.refresh(borrow)

    return borrow
    

@router.post("/{borrow_id}/return",response_model=BorrowRecordResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(BorrowRecord).filter(BorrowRecord.id == borrow_id).first()
    
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    if borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    borrow.return_date = datetime.now(timezone.utc)

    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if book:
        book.status = BookStatus.available

    db.commit()
    db.refresh(borrow)
    return borrow

@router.get("/",response_model=list[BorrowRecordResponse])
def get_borrows(db: Session = Depends(get_db)):
    return db.query(BorrowRecord).all()

@router.get("/user/{user_id}",response_model=list[BorrowRecordResponse])
def get_user_borrows(user_id: int, db: Session = Depends(get_db)):
    return ( db.query(BorrowRecord).filter(BorrowRecord.user_id == user_id).all() )


