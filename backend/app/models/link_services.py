import typing
from datetime import datetime
from pymongo.collection import Collection
from pydantic import error_wrappers
from bson import errors
from bson.objectid import ObjectId
from .schemas import Link
from .serializers import link_serializer


def get_link(link_id: str, collection: Collection) -> Link:
    """
    Return link object or None by given link id value.
    """
    # Convert given str id into ObjectId object
    try:
        link_object_id = ObjectId(link_id)
    except errors.InvalidId as e:
        raise e
    # Get link object
    link_obj = collection.find_one({'_id': link_object_id})
    # Parse data if link object exits
    try:
        return link_serializer(link_obj)
    except error_wrappers.ValidationError:
        raise ValueError('Link does not exists.')


def get_links(collection: Collection) -> typing.List[Link]:
    """
    Return list of Link objects.
    """
    links = collection.find()
    if links:
        # Return reversed list of links
        reversed_list = list(map(lambda x: link_serializer(x), links))
        reversed_list.reverse()
        return reversed_list
    return []


def check_that_link_exists(url: str, collection: Collection) -> bool:
    """
    Check that link with given url exists.
    """
    obj = collection.find_one({'url': url})
    if obj:
        return True
    return False


def add_link(data: Link, collection: Collection) -> Link:
    """
    Add given Link object to the database and return it.
    """
    # Check that link already exists
    if check_that_link_exists(data.url, collection):
        raise ValueError('Link with given url already exists.')
    # Update data with date_added
    payload = data.dict()
    payload.update({'date_added': datetime.utcnow()})
    # Insert data
    obj = collection.insert_one(payload)
    return get_link(str(obj.inserted_id), collection)
