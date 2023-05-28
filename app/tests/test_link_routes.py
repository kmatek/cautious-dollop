from fastapi import status

LINKS_URL = "/api/links/"
CHECK_EXISTS_URL = "/api/links/exists/"


def test_add_link(test_client, create_test_token):
    """
    Test add new link object to the database.
    """
    # Add link
    payload = {
        "url": "https://example.com",
    }
    # Add data
    data = create_test_token
    response = test_client.post(
        LINKS_URL,
        headers={'Authorization': data.get("token")},
        json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data.get("url") == payload.get("url")
    assert response_data.get("added_by") == data.get('user').username
    assert response_data.get("_id")
    assert response_data.get("date_added")


def test_add_link_not_authorized(test_client, test_user_client, test_user_database):
    """
    Test add link not authorized.
    """
    payload = {
        "url": "https://example.com",
    }
    # Add data
    response = test_client.post(LINKS_URL, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_link_that_already_exists(test_client, create_test_token):
    """
    Test add new link object with given url that already exists.
    """
    # Add data
    data = create_test_token
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    response = test_client.post(
        LINKS_URL,
        headers={'Authorization': data.get("token")},
        json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(
        LINKS_URL,
        headers={'Authorization': data.get("token")},
        json=payload
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_add_link_not_allowed_method(test_client):
    """
    Test all not allowed method.
    """
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    # Put
    response = test_client.put(LINKS_URL, json=payload)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Patch
    response = test_client.patch(LINKS_URL, json=payload)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Delete
    response = test_client.delete(LINKS_URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_check_url_exists_not_authorized(test_client, create_test_token):
    """
    Test checking that url exists in the databse being not authorized.
    """
    data = create_test_token

    payload = {
        "url": "https://example.com",
    }
    # Add data
    response = test_client.post(
        LINKS_URL,
        headers={'Authorization': data.get("token")},
        json=payload)
    # Check exists
    url = CHECK_EXISTS_URL + '?url=https://example.com'
    response = test_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_check_url_exists(test_client, create_test_token):
    """
    Test checking that url exists in the databse.
    """
    data = create_test_token

    payload = {
        "url": "https://example.com",
    }
    # Add data
    response = test_client.post(
        LINKS_URL,
        headers={'Authorization': data.get("token")},
        json=payload)
    # Check exists
    url = CHECK_EXISTS_URL + '?url=https://example.com'
    response = test_client.get(
        url, headers={'Authorization': data.get("token")})
    assert response.status_code == status.HTTP_200_OK


def test_check_url_not_exists(test_client, create_test_token):
    """
    Test check that url exists in the databse.
    """
    data = create_test_token

    # Check exists
    url = CHECK_EXISTS_URL + '?url=https://example.com'
    response = test_client.get(
        url, headers={'Authorization': data.get("token")})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_check_url_not_allowed_method(test_client):
    """
    Test check url endpoint not allowe methods.
    """
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    # Add data
    response = test_client.post(LINKS_URL, json=payload)
    # Check exists
    url = CHECK_EXISTS_URL + '?url=https://example.com'

    # Put
    response = test_client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Patch
    response = test_client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Delete
    response = test_client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Post
    response = test_client.post(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_get_links_not_authorized(test_client):
    """
    Test getting links from empty database being not authorized.
    """
    response = test_client.get(LINKS_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_links_with_empty_database(test_client, create_test_token):
    """
    Test get links from empty database.
    """
    data = create_test_token

    response = test_client.get(
        LINKS_URL, headers={'Authorization': data.get('token')})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_links(test_client, create_test_token):
    """
    Test get links from database.
    """
    token_data = create_test_token

    # Add some data
    data = []
    for i in range(30):
        res = test_client.post(
            LINKS_URL,
            headers={'Authorization': token_data.get('token')},
            json={'url': f'https://example{i}.com'}
        )
        data.append(res.json())

    response = test_client.get(
        LINKS_URL, headers={'Authorization': token_data.get('token')})
    assert response.status_code == status.HTTP_200_OK
    for index, obj in enumerate(response.json()):
        assert obj == data[index]


def test_get_links_not_allowed_methods(test_client):
    """
    Test get links not allowed methods.
    """
    # Add some data
    data = []
    for i in range(30):
        res = test_client.post(
            LINKS_URL,
            json={'url': f'https://example{i}.com', 'added_by': 'Someone'}
        )
        data.append(res.json())

    # Put
    response = test_client.put(LINKS_URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Patch
    response = test_client.patch(LINKS_URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Delete
    response = test_client.delete(LINKS_URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_get_link_not_authorized(test_client, create_test_token):
    """
    Test get link object from database being not authorized.
    """
    data = create_test_token

    # Add data
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    res = test_client.post(
        LINKS_URL,
        headers={'Authorization': data.get('token')},
        json=payload
    )
    res_data = res.json()

    url = LINKS_URL + f"{res_data['_id']}"
    response = test_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_link(test_client, create_test_token):
    """
    Test get link object from database.
    """
    data = create_test_token

    # Add data
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    res = test_client.post(
        LINKS_URL,
        headers={'Authorization': data.get('token')},
        json=payload
    )
    res_data = res.json()

    url = LINKS_URL + f"{res_data['_id']}"
    response = test_client.get(
        url, headers={'Authorization': data.get('token')},)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == res_data


def test_get_link_not_allowed_methods(test_client, create_test_token):
    """
    Test get link not allowed methods.
    """
    data = create_test_token

    # Add data
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    res = test_client.post(
        LINKS_URL,
        headers={'Authorization': data.get('token')},
        json=payload
    )
    res_data = res.json()

    url = LINKS_URL + f"{res_data['_id']}"
    # Put
    response = test_client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Post
    response = test_client.post(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Patch
    response = test_client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    # Delete
    response = test_client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_get_link_that_not_exists(test_client, create_test_token):
    """
    Test get link object that now exists from database.
    """
    data = create_test_token

    url = LINKS_URL + "test_id"
    response = test_client.get(
        url, headers={'Authorization': data.get('token')})
    assert response.status_code == status.HTTP_404_NOT_FOUND
