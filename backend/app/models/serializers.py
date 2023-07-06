from pydantic import error_wrappers

from .schemas import Link, UserModel, DBUser


def link_serializer(obj: dict) -> Link:
    """
    Parse link data from database into Link model schema.
    """
    return Link.parse_obj(obj)


def user_serializer(obj: dict) -> UserModel:
    """
    Parse user data from database into UserModel schema.
    """
    try:
        return UserModel.parse_obj(obj)
    except error_wrappers.ValidationError:
        raise ValueError('User does not exists')


def dbuser_serializer(obj: dict) -> DBUser:
    """
    Parse user data from database into DBUser schema.
    """
    try:
        return DBUser.parse_obj(obj)
    except error_wrappers.ValidationError:
        raise ValueError('User does not exists')
