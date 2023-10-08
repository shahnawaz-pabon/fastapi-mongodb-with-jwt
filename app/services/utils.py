from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
