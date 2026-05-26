from sqlalchemy import Column, Integer, String,ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True,nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    publication_year = Column(Integer, index=True, nullable=False)
    status = Column(String, index=True, nullable=False, default="available")
    borrow_records = relationship("BorrowRecord", back_populates="book")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    borrow_records = relationship("BorrowRecord", back_populates="user")

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    return_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")

