from fastapi import APIRouter, Response, status, Depends, HTTPException
from datetime import datetime, timedelta
from app.models.user import UserResponse, CreateUserSchema
from app.db.database import User
from app.services import utils

router = APIRouter()

# [...] register user


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(payload: CreateUserSchema):
    # Check if user already exist
    user = User.find_one({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    #  Hash the password
    payload.password = utils.get_hashed_password(payload.password)
    del payload.passwordConfirm
    payload.role = 'user'
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    return {"status": "success"}
