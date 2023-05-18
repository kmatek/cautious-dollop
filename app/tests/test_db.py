import pytest

from ..models.link_services import add_link, get_link, check_if_link_exist
from ..models.schemas import Link


def test_add_link(test_urls_database):
    """
    Test that add_link service works correct.
    """
    collection = test_urls_database

    data = Link(link='test_link', added_by='test_user')
    add_link(data, collection)

    assert check_if_link_exist(data.link, collection) is True


def test_add_link_that_already_exists(test_urls_database):
    """
    Test uniqueness validator for link field.
    """
    collection = test_urls_database
    # Add link to the database
    data = Link(link='hiper_link', added_by='test_user')
    add_link(data, collection)

    with pytest.raises(ValueError):
        # Try add same data
        add_link(data, collection)


def test_get_link(test_urls_database):
    """
    Test get link from database.
    """
    collection = test_urls_database
    # Add link to the database
    data = Link(link='test_link2', added_by='test_user')
    add_link(data, collection)

    link_obj = get_link(data.link, collection)
    assert link_obj.get('link') == data.link
    assert link_obj.get('added_by') == data.added_by


def test_check_if_link_exists_method(test_urls_database):
    """
    Test checking if link exist in the database.
    """
    collection = test_urls_database
    # Add link to the database
    data = Link(link='test_link3', added_by='test_user')
    add_link(data, collection)

    assert check_if_link_exist(data.link, collection) is True
    assert check_if_link_exist('different_link', collection) is False
