import pytest
from passlib.hash import pbkdf2_sha256
from bson import errors
from bson.objectid import ObjectId
import jwt

from models.schemas import DBUser
from models.user_services import (
    get_hashed_password,
    get_user,
    create_user,
    verify_password,
    get_user_with_password,
    authenticate_user,
    create_access_token
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
        password='password',
    )
    payload = data.dict()
    payload.update({'password': get_hashed_password(data.password)})

    collection.insert_one(payload)
    # Get data
    user_obj = get_user_with_password(data.username, collection)
    assert user_obj.id
    assert user_obj.username == data.username
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
        password='password',
    )
    payload = data.dict()
    payload.update({'password': get_hashed_password(data.password)})
    collection.insert_one(payload)

    obj = authenticate_user(collection, data.username, data.password)

    assert type(obj) == DBUser
    assert obj.username == data.username


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


def test_create_access_token(test_user_database):
    """
    Test create access token.
    """
    payload = {'sub': 'someone'}
    token = create_access_token(payload)
    decoded_value = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded_value.get('exp')
    assert decoded_value.get('sub') == payload.get('sub')


def test_create_user(test_user_database):
    """
    Test add new user to the database.
    """
    collection = test_user_database

    # Add user to the database
    data = DBUser(username='user', password='password')
    obj = create_user(data, collection)

    assert obj.username == data.username
    assert obj.is_admin is False
    assert obj.disabled is False
    assert obj.date_added is not None
    with pytest.raises(AttributeError):
        obj.password

    user_obj = collection.find_one({'_id': ObjectId(obj.id)})
    assert pbkdf2_sha256.verify('password', user_obj.get('password')) is True
