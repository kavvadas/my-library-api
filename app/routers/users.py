from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.dependencies import verify_api_key
from app.models import User,UserRole
from app.schemas import UserResponse, UserCreate


router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(verify_api_key)]
)

@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        or_(User.email == user.email,
            User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400,
                             detail="User with this email or username already exists")
    
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@router.get("/",response_model=list[UserResponse])
def get_users(page: int = 1, size: int = 10, search: str | None = None, db: Session = Depends(get_db)):
    if page < 1 or size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST
                            , detail="Page and size must be positive integers")
    query = db.query(User).order_by(User.id)
    if search:
        query = query.filter(
            or_(
                User.username.ilike(f"%{search}"),
                User.email.ilike(f"%{search}")
            )
        )
    users = query.offset((page-1)*size).limit(size).all()
    return users
        
    