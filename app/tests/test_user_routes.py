from fastapi import status

from models.schemas import DBUser
from models.user_services import create_user

USER_URL = "/api/user"
TOKEN_URL = "/api/user/token"


def test_get_token_user_not_exists(test_user_client):
    """
    Test get token endpoint with wrong data.
    """
    payload = {
        'username': 'someone',
        'password': 'somepassword'
    }
    response = test_user_client.post(TOKEN_URL, data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_token(test_user_client, test_user_database):
    """
    Test get token endpoint.
    """
    # Add data
    collection = test_user_database
    data = DBUser(username='someone1', password='password')
    create_user(data, collection)
    # Get token
    payload = {
        'username': data.username,
        'password': 'password'
    }
    response = test_user_client.post(TOKEN_URL, data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_create_new_user_not_token(test_user_client):
    """
    Test create user endpoint.
    """
    payload = {
        'username': 'someone',
        'password': 'password'
    }
    response = test_user_client.post(USER_URL, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_new_user_not_admin(test_user_client, test_user_database):
    """
    Test create user endpoint.
    """
    # Create no admin user
    collection = test_user_database
    data = DBUser(username='someone1', password='password')
    create_user(data, collection)
    # Get token
    payload = {
        'username': data.username,
        'password': 'password'
    }
    response = test_user_client.post(TOKEN_URL, data=payload)
    token = response.json().get('access_token')
    token_type = response.json().get('token_type')

    payload = {
        'username': 'someone',
        'password': 'password'
    }
    response = test_user_client.post(
        USER_URL,
        headers={'Authorization': f'{token_type} {token}'},
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_new_user_admin(test_user_client, test_user_database):
    """
    Test create user endpoint.
    """
    # Create no admin user
    collection = test_user_database
    data = DBUser(username='someone1', password='password', is_admin=True)
    create_user(data, collection)
    # Get token
    payload = {
        'username': data.username,
        'password': 'password'
    }
    response = test_user_client.post(TOKEN_URL, data=payload)
    token = response.json().get('access_token')
    token_type = response.json().get('token_type')

    payload = {
        'username': 'someone',
        'password': 'password'
    }
    response = test_user_client.post(
        USER_URL,
        headers={'Authorization': f'{token_type} {token}'},
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert 'username' in response.json()
    assert 'is_admin' in response.json()
    assert 'password' not in response.json()
    assert 'disabled' in response.json()
    assert response.json().get('is_admin') is False
