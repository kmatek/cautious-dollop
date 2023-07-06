from fastapi import status

from models.schemas import DBUser
from models.user_services import create_user

USER_URL = "/api/user"
TOKEN_URL = USER_URL + "/token"
USER_DETAIL_URL = USER_URL + "/me"
USER_PASSWORD_UPDATE = USER_URL + "/update-password"


def test_get_token_user_not_exists(test_user_client):
    """
    Test get token endpoint with wrong data.
    """
    payload = {
        'email': 'example@email.com',
        'password': 'somepassword'
    }
    response = test_user_client.post(TOKEN_URL, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_token(test_user_client, test_user_database):
    """
    Test get token endpoint.
    """
    # Add data
    collection = test_user_database
    data = DBUser(
        username='someone1',
        email='example@email.com',
        password='password'
    )
    create_user(data, collection)
    # Get token
    payload = {
        'email': data.email,
        'password': 'password'
    }
    response = test_user_client.post(TOKEN_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_get_token_not_allowed_methods(test_user_client, test_user_database):
    """
    Test get token not allowed methods.
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
    # Put
    response = test_user_client.put(TOKEN_URL, data=payload)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Patch
    response = test_user_client.patch(TOKEN_URL, data=payload)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Delete
    response = test_user_client.delete(TOKEN_URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Get
    response = test_user_client.put(TOKEN_URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


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


def test_create_new_user_not_admin(test_user_client, create_test_token):
    """
    Test create user endpoint.
    """
    # Get data
    data = create_test_token
    token = data.get('token')

    payload = {
        'username': 'someone',
        'password': 'password'
    }
    response = test_user_client.post(
        USER_URL,
        headers={'Authorization': token},
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_new_user_as_admin(test_user_client, create_test_token_admin):
    """
    Test create user endpoint.
    """
    # Get data
    data = create_test_token_admin
    token = data.get('token')

    payload = {
        'username': 'someone',
        'password': 'password',
        'email': 'example2@email.com'
    }
    response = test_user_client.post(
        USER_URL,
        headers={'Authorization': token},
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert payload.get('username') == response.json().get('username')
    assert 'password' not in response.json()
    assert response.json().get('disabled') is False
    assert response.json().get('is_admin') is False
    assert payload.get('email') == response.json().get('email')


def test_create_new_user_with_wrong_email(test_user_client, create_test_token_admin):
    """
    Test create user endpoint.
    """
    # Get data
    data = create_test_token_admin
    token = data.get('token')

    payload = {
        'username': 'someone',
        'password': 'password',
        'email': 'exampleemail.com'
    }
    response = test_user_client.post(
        USER_URL,
        headers={'Authorization': token},
        json=payload,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert 'username' not in response.json()
    assert 'password' not in response.json()
    assert 'disabled' not in response.json()
    assert 'is_admin' not in response.json()
    assert 'email' not in response.json()


def test_create_new_user_with_email_already_exists(test_user_client, create_test_token_admin):
    """
    Test create user endpoint with given email that already exists.
    """
    # Get data
    data = create_test_token_admin
    token = data.get('token')

    payload = {
        'username': 'someone',
        'password': 'password',
        'email': 'example@email.com'
    }
    # Already exists
    response = test_user_client.post(
        USER_URL,
        headers={'Authorization': token},
        json=payload,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_new_user_not_allowed_methods(test_user_client, test_user_database):
    """
    Test create new user endpoint not allowed methods.
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
    # Put
    response = test_user_client.put(
        USER_URL,
        headers={'Authorization': f'{token_type} {token}'},
        json=payload,
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Patch
    response = test_user_client.patch(
        USER_URL,
        headers={'Authorization': f'{token_type} {token}'},
        json=payload,
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Get
    response = test_user_client.get(
        USER_URL,
        headers={'Authorization': f'{token_type} {token}'},
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Delete
    response = test_user_client.delete(
        USER_URL,
        headers={'Authorization': f'{token_type} {token}'},
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_current_user(test_user_client, create_test_token):
    """
    Test get current user endpoint.
    """
    # Get data
    data = create_test_token
    token = data.get('token')
    user = data.get('user')
    # Get user data with endpoint
    response = test_user_client.get(
        USER_DETAIL_URL,
        headers={'Authorization': token},)
    assert response.status_code == 200
    assert 'password' not in response.json()
    assert response.json().get('username') == user.username
    assert response.json().get('disabled') == user.disabled
    assert response.json().get('is_admin') == user.is_admin
    assert response.json().get('email') == user.email


def test_current_user_not_allowed_methods(test_user_client, test_user_database):
    """
    Test current user endpoint not allowed methods.
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
    token = response.json().get('access_token')
    token_type = response.json().get('token_type')

    # Put
    response = test_user_client.put(
        USER_DETAIL_URL,
        headers={'Authorization': f'{token_type} {token}'},)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Patch
    response = test_user_client.patch(
        USER_DETAIL_URL,
        headers={'Authorization': f'{token_type} {token}'},)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Delete
    response = test_user_client.delete(
        USER_DETAIL_URL,
        headers={'Authorization': f'{token_type} {token}'},)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Post
    response = test_user_client.post(
        USER_DETAIL_URL,
        headers={'Authorization': f'{token_type} {token}'},)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_current_user_no_user(test_user_client):
    """
    Test get current user endpoint.
    """
    # Get user data with endpoint
    response = test_user_client.get(USER_DETAIL_URL)
    assert response.status_code == 401
    assert 'password' not in response.json()
    assert 'username' not in response.json()


def test_update_user_password(test_user_client, create_test_token):
    """
    Test update user password endpoint.
    """
    # Add data
    data = create_test_token
    user = data.get('user')
    token = data.get('token')
    # Update password with wrtoing old password
    payload = {
        'old_password': 'wrong_password',
        'new_password': 'new_password'
    }
    response = test_user_client.put(
        USER_PASSWORD_UPDATE,
        headers={'Authorization': token},
        json=payload,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Try get token with new password
    payload = {
        'email': user.email,
        'password': 'new_password'
    }
    response = test_user_client.post(TOKEN_URL, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Update password with correct old password
    payload = {
        'old_password': 'password',
        'new_password': 'new_password'
    }
    response = test_user_client.put(
        USER_PASSWORD_UPDATE,
        headers={'Authorization': token},
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK

    # Try get token with new password
    payload = {
        'email': user.email,
        'password': 'new_password'
    }
    response = test_user_client.post(TOKEN_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
