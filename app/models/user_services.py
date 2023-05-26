from datetime import datetime, timedelta

from pymongo.collection import Collection
from pydantic import error_wrappers
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId
from bson import errors
import jwt

from .schemas import UserModel, DBUser
from .serializers import user_serializer, dbuser_serializer
from app.config import settings


def get_hashed_password(password: str) -> str:
    """
    Return hashed given password.
    """
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Return True or False depens on password matching.
    """
    return pbkdf2_sha256.verify(password, hashed_password)


def get_user(user_id: str, collection: Collection) -> UserModel:
    """
    Get user from database.
    """
    # Convert given str id into ObjectId object
    try:
        user_id = ObjectId(user_id)
    except errors.InvalidId as e:
        raise e

    # Get user from database
    user_obj = collection.find_one({'_id': user_id})

    # Parse data into UserModel
    try:
        return user_serializer(user_obj)
    except error_wrappers.ValidationError:
        raise ValueError('User does not exists')


def get_user_with_password(username: str, collection: Collection) -> DBUser:
    """
    Get user with hashed password from databse.
    """
    # Get user from database
    user_obj = collection.find_one({'username': username})
    # Parse data into UserModel
    try:
        return dbuser_serializer(user_obj)
    except error_wrappers.ValidationError:
        raise ValueError('User does not exists')


def authenticate_user(collection: Collection, username: str, password: str) -> bool | DBUser:
    """
    Aunthenticate user with given username and password.
    Return boolean or DBUser value.
    """
    # Get user
    try:
        user = get_user_with_password(username, collection)
        # Verify password
        if not verify_password(password, user.password):
            return False
        return user
    except ValueError:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create encoded access token.
    """
    # Copy given data
    to_encode = data.copy()
    # Set expire time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Update dict
    to_encode.update({'exp': expire})
    # Create token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_user(data: DBUser, collection: Collection) -> UserModel:
    """
    Add user to database.
    """
    # Hash user password
    user_pwd = get_hashed_password(data.password)
    data.password = user_pwd

    # Update date_added field
    data.date_added = datetime.utcnow()

    # Add user to the database
    obj = collection.insert_one(data.dict())

    # Return UserModel schema
    return get_user(str(obj.inserted_id), collection)
