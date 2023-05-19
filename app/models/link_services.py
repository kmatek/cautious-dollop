import typing
from pymongo.collection import Collection
from pydantic.error_wrappers import ValidationError
from bson.objectid import ObjectId
from .schemas import Link
from .serializers import link_endpoint_serializer


def get_link(link_id: str, collection: Collection) -> Link | None:
    """
    Return link object or None by given link id value.
    """
    # Convert given str id into ObjectId object
    link_object_id = ObjectId(link_id)
    # Get link_obj
    link_obj = collection.find_one({'_id': link_object_id})
    # Parse data if link object exits
    try:
        return link_endpoint_serializer(link_obj)
    except ValidationError:
        raise ValueError('Link does not exists.')


def get_links(collection: Collection) -> typing.List[Link]:
    """
    Return list of Link objects.
    """
    links = collection.find()
    if links:
        return list(map(lambda x: link_endpoint_serializer(x), links))
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

    obj = collection.insert_one(data.dict())
    return get_link(obj.inserted_id, collection)
