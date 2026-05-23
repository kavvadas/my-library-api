from pydantic import BaseModel, ConfigDict
from enum import Enum

class BookStatus(str, Enum):
    available = "available"
    checked_out = "checked_out"

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    status: BookStatus

class BookCreate(BookBase):
    pass

class BookDelete(BaseModel):
    id: int

class BookUpdate(BaseModel):
    id: int
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    publication_year: int | None = None
    status: BookStatus | None = None

class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)



