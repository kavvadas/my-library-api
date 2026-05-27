from fastapi import Header, HTTPException, Depends
from app.config import settings
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models import User
from app.utils.security import decode_token

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)):

    credentials_exception = HTTPException(status_code= 401,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise credentials_exception
    
    return user
    
