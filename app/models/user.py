from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from typing import Union


class UserBaseSchema(BaseModel):
    name: str
    email: str
    photo: str
    role: str = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
