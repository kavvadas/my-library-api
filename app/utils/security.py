from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
import os

JWT_KEY = os.getenv("JWT_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes = 15))
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,JWT_KEY,algorithm =ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token,JWT_KEY,algorithms =[ALGORITHM])    