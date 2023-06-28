from datetime import datetime
from unittest.mock import patch

import pytest
from passlib.hash import pbkdf2_sha256
from bson import errors
from bson.objectid import ObjectId
import jwt
from freezegun import freeze_time
from pydantic import error_wrappers

from models.schemas import DBUser
from models.user_services import (
    get_hashed_password,
    get_user,
    create_user,
    verify_password,
    get_user_with_password,
    authenticate_user,
    create_access_token,
    update_user_password,
)
from app.config import settings


def test_get_hashed_password():
    """
    Test hashing password method.
    """
    password = 'example-password'
    hashed_password = get_hashed_password(password)

    assert pbkdf2_sha256.verify(password, hashed_password) is True
    assert pbkdf2_sha256.verify('wrong-password', hashed_password) is False


def test_verify_password():
    """
    Test verify password method.
    """
    password = 'example-password'
    hashed_password = get_hashed_password(password)

    assert verify_password(password, hashed_password) is True
    assert verify_password('wrong-passowrd', hashed_password) is False


def test_get_user_that_not_exists(test_user_database):
    """
    Test get user that not exists from database.
    """
    collection = test_user_database

    # Add user to the database
    data = DBUser(
        username='user1',
        password='password',
    )
    obj = collection.insert_one(data.dict())
    user_id = str(obj.inserted_id)
    # Get data
    with pytest.raises(errors.InvalidId):
        get_user('invalid_id', collection)

    assert get_user(user_id, collection).id == user_id


def test_get_user(test_user_database):
    """
    Test get user from database.
    """
    collection = test_user_database

    # Add user to the database
    data = DBUser(
        username='user1',
        password='password',
    )
    payload = data.dict()
    payload.update({'password': get_hashed_password(data.password)})

    obj = collection.insert_one(payload)
    user_id = str(obj.inserted_id)
    # Get data
    user_obj = get_user(user_id, collection)
    assert user_obj.id == user_id
    assert user_obj.username == data.username
    with pytest.raises(AttributeError):
        user_id.password

    user_obj = collection.find_one({'_id': ObjectId(user_id)})
    assert pbkdf2_sha256.verify(data.password, user_obj.get('password')) is True


def test_get_user_with_password(test_user_database):
    """
    Test get user data with password from database.
    """
    collection = test_user_database

    # Add user to the database
    data = DBUser(
        username='user1',
        email='example@email.com',
        password='password',
    )
    payload = data.dict()
    payload.update({'password': get_hashed_password(data.password)})

    collection.insert_one(payload)
    # Get data
    user_obj = get_user_with_password(data.email, collection)
    assert user_obj.id
    assert user_obj.username == data.username
    assert user_obj.email == data.email
    assert user_obj.password
    assert pbkdf2_sha256.verify(data.password, user_obj.password) is True


def test_authenicate_user_method(test_user_database):
    """
    Test authenticate user method.
    """
    # Add user to the databse.
    collection = test_user_database
    data = DBUser(
        username='user1',
        email='example@email.com',
        password='password',
    )
    payload = data.dict()
    payload.update({'password': get_hashed_password(data.password)})
    collection.insert_one(payload)

    obj = authenticate_user(collection, data.email, data.password)

    assert type(obj) == DBUser
    assert obj.username == data.username
    assert obj.email == data.email


def test_authenicate_user_method_with_wrong_username(test_user_database):
    """
    Test authenticate user method with fake data.
    """
    # Add user to the databse.
    collection = test_user_database
    data = DBUser(
        username='user1',
        password='password',
    )
    payload = data.dict()
    payload.update({'password': get_hashed_password(data.password)})
    collection.insert_one(payload)

    obj = authenticate_user(collection, 'wrong username', data.password)
    assert obj is False


def test_authenicate_user_method_with_wrong_password(test_user_database):
    """
    Test authenticate user method with fake data.
    """
    # Add user to the databse.
    collection = test_user_database
    data = DBUser(
        username='user1',
        password='password',
    )
    payload = data.dict()
    payload.update({'password': get_hashed_password(data.password)})
    collection.insert_one(payload)

    obj = authenticate_user(collection, data.username, 'wrong-password')
    assert obj is False


@freeze_time("2023-05-27T10:00:00Z")
def test_create_access_token(test_user_database):
    """
    Test create access token.
    """
    # Patch value
    with patch.object(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 10):
        payload = {'sub': 'someone'}
        token = create_access_token(payload)
        decoded_value = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert datetime.fromtimestamp(decoded_value.get('exp')) > datetime.utcnow()
        assert decoded_value.get('sub') == payload.get('sub')

        # Check token expired
        freezer = freeze_time(f"2023-05-27T10:{settings.ACCESS_TOKEN_EXPIRE_MINUTES + 1}:00Z")
        freezer.start()

        with pytest.raises(jwt.exceptions.ExpiredSignatureError):
            decoded_value = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        freezer.stop()


def test_create_user(test_user_database):
    """
    Test add new user to the database.
    """
    collection = test_user_database

    # Add user to the database
    data = DBUser(
        username='user', password='password', email='example@email.com')
    obj = create_user(data, collection)

    assert obj.username == data.username
    assert obj.email == data.email
    assert obj.is_admin is False
    assert obj.disabled is False
    assert obj.date_added is not None
    with pytest.raises(AttributeError):
        obj.password

    user_obj = collection.find_one({'_id': ObjectId(obj.id)})
    assert pbkdf2_sha256.verify('password', user_obj.get('password')) is True


def test_create_user_invalid_email():
    """
    Test add new user to the database.
    """
    # Add user to the database
    with pytest.raises(error_wrappers.ValidationError):
        DBUser(username='user', password='password', email='exampleail.com')


def test_check_user_already_exists(test_user_database):
    """
    Test checking that user with given email already exists.
    """
    collection = test_user_database

    # Add user to the database
    data = DBUser(
        username='user', password='password', email='example@email.com')
    create_user(data, collection)

    with pytest.raises(ValueError):
        create_user(data, collection)


def test_update_user_password(test_user_database):
    """
    Test update user password.
    """
    collection = test_user_database

    # Add user to the database
    data = DBUser(
        username='user', password='password',
    )
    obj = create_user(data, collection)

    # Update password with wrong old_password
    with pytest.raises(ValueError):
        update_user_password(
            user_id=obj.id, old_password='drowssap',
            new_password='new-password', collection=collection
        )

    # Update password
    update_user_password(
        user_id=obj.id, old_password='password',
        new_password='new-password', collection=collection
    )
    user_obj = collection.find_one({'_id': ObjectId(obj.id)})
    assert pbkdf2_sha256.verify('new-password', user_obj.get('password')) is True
