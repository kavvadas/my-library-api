from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.dependencies import verify_api_key
from app.models import User,UserRole
from app.schemas import UserResponse, UserCreate, UserUpdate
from app.utils.security import hash_password

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
        hashed_password = hash_password(user.password)
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
            or_(User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"))
        )
    users = query.offset((page-1)*size).limit(size).all()
    return users
        
@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/role/{role}",response_model=list[UserResponse])
def get_users_by_role(role: UserRole, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.role == role).all()
    return users

@router.put("/{user_id}",response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    existing_user = db.query(User).filter(
        or_(User.email == user_update.email,
            User.username == user_update.username),
        User.id != user_id
    ).first()
    if existing_user:
        raise HTTPException(status_code=400,
                             detail="Another user with this email or username already exists")
    
    data = user_update.model_dump(exclude_unset=True)
    if "password" in data:
        data["hashed_password"] = hash_password(data.pop("password"))
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()