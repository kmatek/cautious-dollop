from pymongo.collection import Collection
from .schemas import Link


def get_link(link: str, collection: Collection) -> Link | None:
    """
    Return link object or None by given link value.
    """
    link_obj = collection.find_one({'link': link})
    return link_obj


def check_if_link_exist(link: str, collection: Collection) -> bool:
    """
    Check that link object exists.
    """
    link_obj = get_link(link, collection)
    if link_obj:
        return True
    return False


def add_link(data: Link, collection: Collection) -> Link:
    """
    Add new link model to the database.
    """
    # Check that link dont exists
    exists = check_if_link_exist(data.link, collection)
    if exists:
        raise ValueError('Given link already exists.')

    link_obj = collection.insert_one(data.dict())
    return link_obj
