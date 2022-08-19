from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.database.init_db import SessionLocal
from app.database import init_db

get_db = init_db.get_db
SECRET_KEY = "40685ce01419b8e886136d45c37fb061b02a1060e3b5cbec83512234fe617ae3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token(http_authorization_credentials=Depends(reusable_oauth2), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(http_authorization_credentials.credentials,
                             SECRET_KEY, algorithms=[ALGORITHM])
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials",
        )
