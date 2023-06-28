import pytest
from fastapi.testclient import TestClient

from db.database import client
from app.main import app
from routes.links import get_collection
from routes.users import get_user_collection
from models.schemas import DBUser
from models.user_services import create_user


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
def test_user_database():
    """
    Connect to the test databse.
    """
    test_db = client.test_user_database

    yield test_db.test_user_database
    # Clean up
    test_db.test_user_database.drop()


@pytest.fixture()
def test_client(test_urls_database):
    app.dependency_overrides[get_collection] = lambda: test_urls_database
    yield TestClient(app)
    app.dependency_overrides.pop(get_collection)  # Clean up the dependency override after tests


@pytest.fixture()
def test_user_client(test_user_database):
    app.dependency_overrides[get_user_collection] = lambda: test_user_database
    yield TestClient(app)
    app.dependency_overrides.pop(get_user_collection)  # Clean up the dependency override after tests


@pytest.fixture()
def create_test_token(test_user_client, test_user_database):
    """
    Helper function that will create token
    """
    # Get token
    collection = test_user_database
    data = DBUser(
        username='someone1',
        email='example@email.com',
        password='password'
    )
    user = create_user(data, collection)
    # Get token
    payload = {
        'email': data.email,
        'password': 'password'
    }
    response = test_user_client.post('/api/user/token', json=payload)
    token = response.json().get('access_token')
    token_type = response.json().get('token_type')
    return {'user': user, 'token': f'{token_type} {token}'}


@pytest.fixture()
def create_test_token_admin(test_user_client, test_user_database):
    """
    Helper function that will create token
    """
    # Get token
    collection = test_user_database
    data = DBUser(
        username='someone1',
        email='example@email.com',
        password='password',
        is_admin=True
    )
    user = create_user(data, collection)
    # Get token
    payload = {
        'email': data.email,
        'password': 'password'
    }
    response = test_user_client.post('/api/user/token', json=payload)
    token = response.json().get('access_token')
    token_type = response.json().get('token_type')
    return {'user': user, 'token': f'{token_type} {token}'}
