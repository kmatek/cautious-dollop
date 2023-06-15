from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pymongo.collection import Collection
import jwt

from db.database import user_collection
from app.config import settings
from models.user_services import (
    get_user_with_password,
    authenticate_user,
    create_access_token,
    create_user,
    update_user_password
)
from models.schemas import Token, DBUser, UserModel, PasswordUpdate, TokenIn

router = APIRouter(
    prefix='/api/user',
    tags=['User']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependencies
async def get_user_collection():
    """
    Return user db collection.
    """
    yield user_collection


async def get_current_active_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Collection, Depends(get_user_collection)]
):
    """
    Get current active user dependency.
    """
    # Credentials exception
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentails or token expired.",
        headers={'WWW-Authenticate': 'Bearer'}
    )
    # Decode given token and get username
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        raise credential_exception
    # Get user with decoded username
    try:
        user = get_user_with_password(username, db)
    except ValueError:
        raise credential_exception
    # Check that user is active
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not active."
        )
    return user


async def get_admin_user(
    current_user: Annotated[DBUser, Depends(get_current_active_user)]
):
    """
    Get current active user that is admin dependency.
    """
    # Check if user is admin
    if current_user.is_admin:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Must be an admin user.')


# Endpoints
@router.post('/token', response_model=Token, status_code=status.HTTP_201_CREATED)
async def get_token(
    data: TokenIn,
    db: Annotated[Collection, Depends(get_user_collection)]
) -> dict:
    """
    Get JWT token.
    """
    # Get user
    user = authenticate_user(db, data.email, data.password)
    # Check that user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inavlid email or password.",
            headers={'WWW-Authenticate': 'Bearer'}
        )
    # Create access token
    access_token = create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': settings.TOKEN_TYPE}


@router.post('/', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    data: DBUser,
    db: Annotated[Collection, Depends(get_user_collection)],
    admin: Annotated[DBUser, Depends(get_admin_user)]
) -> UserModel:
    """
    Create new user.
    """
    # Return user
    try:
        return create_user(data, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get('/me', response_model=UserModel, status_code=status.HTTP_200_OK)
async def user_detail(user: Annotated[UserModel, Depends(get_current_active_user)]):
    """
    Get current user by given token.
    """
    return user


@router.put('/update-password', response_model=UserModel, status_code=status.HTTP_200_OK)
async def update_password(
    data: PasswordUpdate,
    db: Annotated[Collection, Depends(get_user_collection)],
    user: Annotated[UserModel, Depends(get_current_active_user)]
) -> UserModel:
    """
    Update current user password.
    """
    # Update given password and return user
    try:
        return update_user_password(
            user.id, db, data.new_password, data.old_password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
