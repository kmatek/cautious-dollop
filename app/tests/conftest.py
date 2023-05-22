import pytest
from fastapi.testclient import TestClient
from db.database import client
from app.main import app
from routes.links import get_collection


@pytest.fixture()
def test_urls_database():
    """
    Connect to the test databse.
    """
    test_db = client.test_urls_db

    yield test_db.test_urls
    # Clean up
    test_db.test_urls.drop()


@pytest.fixture()
def test_client(test_urls_database):
    app.dependency_overrides[get_collection] = lambda: test_urls_database
    yield TestClient(app)
    app.dependency_overrides.pop(get_collection)  # Clean up the dependency override after tests
