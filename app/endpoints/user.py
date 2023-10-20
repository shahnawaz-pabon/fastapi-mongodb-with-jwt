from fastapi import APIRouter, Response, status, HTTPException, Depends
from datetime import datetime, timedelta
from app.models.user import UserResponse, CreateUserSchema, LoginUserSchema
from app.db.database import User
from app.services import utils
from app.core.config import settings
from app.serializers.userSerializers import userEntity, userResponseEntity
from app.services.utils import get_current_user

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
    new_user = userResponseEntity(User.find_one({'_id': result.inserted_id}))
    return {"status": "success", "user": new_user}


# [...] login user
@router.post('/login')
def login(payload: LoginUserSchema, response: Response):
    # Check if the user exist
    db_user = User.find_one({'email': payload.email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    user = userEntity(db_user)

    # Check if the password is valid
    if not utils.verify_password(payload.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create access token
    access_token = utils.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = utils.create_refresh_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, settings.ACCESS_TOKEN_EXPIRES_IN,
                        settings.ACCESS_TOKEN_EXPIRES_IN, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        settings.REFRESH_TOKEN_EXPIRES_IN, settings.REFRESH_TOKEN_EXPIRES_IN, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', settings.ACCESS_TOKEN_EXPIRES_IN,
                        settings.ACCESS_TOKEN_EXPIRES_IN, '/', None, False, False, 'lax')

    # Send both access
    return {'status': 'success', 'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}


@router.get('/me', response_model=UserResponse)
def get_me(email: str = Depends(get_current_user)):
    user = userResponseEntity(User.find_one({'email': email}))
    return {"status": "success", "user": user}
