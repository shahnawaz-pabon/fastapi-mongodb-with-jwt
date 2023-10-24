from passlib.context import CryptContext
import os
from pydantic import ValidationError
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated, Union
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.db.database import User
from app.models.user import TokenPayload, UserBaseSchema

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_security = HTTPBearer()

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_time: int = None) -> str:
    if expires_time is not None:
        expires_time = datetime.utcnow() + expires_time
    else:
        expires_time = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)

    to_encode = {"exp": expires_time, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_PRIVATE_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_time: int = None) -> str:
    if expires_time is not None:
        expires_time = datetime.utcnow() + expires_time
    else:
        expires_time = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN)

    to_encode = {"exp": expires_time, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_PRIVATE_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt


def get_user(email):
    user = User.find_one({'email': email})
    return user


async def get_current_user(access_token: HTTPAuthorizationCredentials = Depends(bearer_security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        payload = jwt.decode(access_token.credentials, settings.JWT_PRIVATE_KEY,
                             algorithms=[settings.JWT_ALGORITHM])

        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(token_data.sub)

    if user is None:
        raise credentials_exception

    return UserBaseSchema(**user)
