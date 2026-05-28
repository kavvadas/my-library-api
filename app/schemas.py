from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import EmailStr

class BookStatus(str, Enum):
    available = "available"
    checked_out = "checked_out"

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int

class BookCreate(BookBase):
    pass

class BookDelete(BaseModel):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    status: Optional[BookStatus] = None

class BookResponse(BookBase):
    id: int
    status: BookStatus
    model_config = ConfigDict(from_attributes=True)

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    username: str
    email: EmailStr



class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
class UserResponse(UserBase):
    id: int
    username: str
    role: UserRole  
    model_config = ConfigDict(from_attributes=True)


class BorrowRecordBase(BaseModel):
    book_id: int


class BorrowRecordCreate(BorrowRecordBase):
    pass

class BorrowRecordReturn(BorrowRecordBase):
    return_date: datetime

class BorrowRecordResponse(BaseModel):
    id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    book: BookResponse
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)

class BorrowRecordUserResponse(BaseModel):
    id:int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    book: BookResponse

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer" #token_type is always bearer in this case



