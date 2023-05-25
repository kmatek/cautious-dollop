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
    return UserModel.parse_obj(obj)


def dbuser_serializer(obj: dict) -> DBUser:
    """
    Parse user data from database into DBUser schema.
    """
    return DBUser.parse_obj(obj)
