from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional

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
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    status: Optional[str] = None

class BookResponse(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)



