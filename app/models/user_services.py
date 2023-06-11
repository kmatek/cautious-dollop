from datetime import datetime, timedelta

from pymongo.collection import Collection
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


def get_raw_user_data(collection: Collection, **kwargs) -> dict:
    """
    Return raw user data.
    """
    if '_id' in kwargs and type(kwargs.get('_id')) == str:
        # Convert given str id into ObjectId object
        try:
            kwargs.update({'_id': ObjectId(kwargs.get('_id'))})
        except errors.InvalidId as e:
            raise e

    return collection.find_one(kwargs)


def get_user(user_id: str, collection: Collection) -> UserModel:
    """
    Get user from database.
    """
    # Get user from database
    user_obj = get_raw_user_data(collection, _id=user_id)

    # Parse data into UserModel
    return user_serializer(user_obj)


def get_user_with_password(username: str, collection: Collection) -> DBUser:
    """
    Get user with hashed password from databse.
    """
    # Get user from database
    user_obj = get_raw_user_data(collection, username=username)

    # Parse data into UserModel
    return dbuser_serializer(user_obj)


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


def create_access_token(data: dict):
    """
    Create encoded access token.
    """
    # Copy given data
    to_encode = data.copy()
    # Set expire time
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Update dict
    to_encode.update({'exp': expire})
    # Create token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def check_that_user_exists(email: str, collection: Collection) -> bool:
    """
    Check that link with given url exists.
    """
    obj = get_raw_user_data(collection, email=email)
    if obj:
        return True
    return False


def create_user(data: DBUser, collection: Collection) -> UserModel:
    """
    Add user to database.
    """
    # Check that user with given email exists
    exists = check_that_user_exists(data.email, collection)
    if exists:
        raise ValueError('User with this email already exists.')

    # Hash user password
    user_pwd = get_hashed_password(data.password)
    data.password = user_pwd

    # Update date_added field
    data.date_added = datetime.utcnow()

    # Add user to the database
    obj = collection.insert_one(data.dict())

    # Return UserModel schema
    return get_user(obj.inserted_id, collection)


def update_user_password(
    user_id: str, collection: Collection,
    new_password: str, old_password: str
) -> UserModel:
    """
    Update user password.
    """
    # Get user_from database
    user = get_raw_user_data(collection, _id=user_id)

    # Check that user exists
    if not user:
        raise ValueError('User does not exists.')

    # Check that given old password is correct
    if not verify_password(old_password, user.get('password')):
        raise ValueError('Old password is incorrect.')

    # Hash user password
    user_pwd = get_hashed_password(new_password)

    # Update user password
    obj = collection.update_one(
        {'_id': ObjectId(user_id)}, {'$set': {'password': user_pwd}})

    if obj.modified_count == 0:
        raise ValueError('User does not exists.')

    # Parse data into UserModel
    return get_user(user_id, collection)
