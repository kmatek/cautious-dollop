import pytest
from db.database import client


@pytest.fixture()
def test_urls_database():
    """
    Connect to the test databse.
    """
    test_db = client.test_urls_db

    yield test_db.test_urls
    # Clean up
    test_db.test_urls.drop()
