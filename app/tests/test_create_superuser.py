from create_superuser import create_superuser


def test_create_superuser(test_user_database):
    """
    Test add an admin user to the database.
    """
    collection = test_user_database

    username = 'test-username'
    password = 'test-password'

    create_superuser(username, password, collection)

    obj = collection.find_one({'username': username})
    assert obj.get('username') == username
    assert obj.get('is_admin') is True
    assert obj.get('password') != password
