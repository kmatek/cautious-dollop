import typing
from pymongo.collection import Collection
from pydantic.error_wrappers import ValidationError
from bson.objectid import ObjectId
from .schemas import Link
from .serializers import link_seriializer


def get_link(link_id: ObjectId, collection: Collection) -> Link | None:
    """
    Return link object or None by given link id value.
    """
    link_obj = collection.find_one({'_id': link_id})
    # Parse data if link object exits
    try:
        return link_seriializer(link_obj)
    except ValidationError:
        raise ValueError('Link does not exists.')


def get_links(collection: Collection) -> typing.List[Link]:
    """
    Return list of Link objects.
    """
    links = collection.find()
    if links:
        return list(map(lambda x: link_seriializer(x), links))
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
