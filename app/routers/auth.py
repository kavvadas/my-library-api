from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import verify_api_key
from app.models import User
from app.schemas import LoginRequest,TokenResponse
from app.utils.security import verify_password,create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login",response_model=TokenResponse,status_code=status.HTTP_202_ACCEPTED)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=401,
                            detail="Invalid credentials")
    if not  verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401,
                            detail="Invalid credentials")
    

    token = create_access_token(
        data = {"sub":str(user.id),
                "role":user.role}
    )
    return {"access_token":token, "token_type":"bearer"}
    
