from datetime import datetime

from pymongo.collection import Collection
from pydantic import error_wrappers
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId
from bson import errors

from .schemas import UserModel, DBUser
from .serializers import user_serializer


def get_hashed_password(password: str) -> str:
    """
    Return hashed given password.
    """
    return pbkdf2_sha256.hash(password)


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
