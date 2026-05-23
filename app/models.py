from sqlalchemy import Column, Integer, String
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True,nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    publication_year = Column(Integer, index=True, nullable=False)
    status = Column(String, index=True, nullable=False)
