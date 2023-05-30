import pytest
from bson.objectid import ObjectId
from bson import errors
from pydantic import error_wrappers

from models.link_services import get_link, get_links, add_link
from models.schemas import Link


def test_get_link(test_urls_database):
    """
    Test get link from database.
    """
    collection = test_urls_database
    # Add link to the database
    data = Link(url='https://example.com', added_by='test_user')
    obj = collection.insert_one(data.dict())
    link_obj = get_link(obj.inserted_id, collection)
    assert link_obj.url == data.url
    assert link_obj.added_by == data.added_by
    assert type(link_obj) is Link
    assert type(link_obj.id) is str


def test_get_link_with_wrong_link(test_urls_database):
    """
    Test get link from database.
    """
    # Add link to the database
    with pytest.raises(error_wrappers.ValidationError):
        Link(url='test_link', added_by='test_user')


def test_get_link_with_invalid_id(test_urls_database):
    """
    Test get link with wrong id from database.
    """
    collection = test_urls_database
    # Add link to the database
    data = Link(url='https://example.com', added_by='test_user')
    collection.insert_one(data.dict())
    # Get data
    with pytest.raises(errors.InvalidId):
        get_link('invalid_id', collection)


def test_get_link_if_not_exists(test_urls_database):
    """
    Test get link from database.
    """
    collection = test_urls_database
    # Add link to the database
    custom_id = ObjectId(b'foo-bar-quux')
    data = Link(_id=custom_id, url='https://example.com', added_by='test_user')
    with pytest.raises(ValueError):
        get_link(data.id, collection)


def test_get_links(test_urls_database):
    """
    Test return list of Link objects
    """
    collection = test_urls_database
    # Add some links to the database
    insert_data_dict = {_: Link(url=f'https://example{_}.com', added_by='test_user')  for _ in range(12)} # noqa
    for _, data in insert_data_dict.items():
        collection.insert_one(data.dict())

    links = get_links(collection)
    assert type(links) is list
    assert type(links[0]) is Link

    for index, link in enumerate(links):
        assert insert_data_dict[index].added_by == link.added_by
        assert insert_data_dict[index].url == link.url
        assert type(link) is Link
        assert type(link.id) is str


def test_get_links_if_empty(test_urls_database):
    """
    Test return empty list of Link objects.
    """
    collection = test_urls_database

    links = get_links(collection)
    assert type(links) is list
    assert bool(links) is False


def test_add_link(test_urls_database):
    """
    Test add new link to the database.
    """
    collection = test_urls_database
    # Add new link
    data = Link(url='https://example.com', added_by='test_user')
    link_obj = add_link(data, collection)

    assert link_obj.url == data.url
    assert link_obj.added_by == data.added_by
    assert type(link_obj) is Link
    assert type(link_obj.id) is str


def test_add_link_already_exists(test_urls_database):
    """
    Test add new link to the database.
    """
    collection = test_urls_database
    # Add new link
    data = Link(url='https://example.com', added_by='test_user')
    add_link(data, collection)

    with pytest.raises(ValueError):
        add_link(data, collection)
