from fastapi import status

LINKS_URL = "/api/links/"
CHECK_EXISTS_URL = "/api/links/exists/"


def test_add_link(test_client):
    """
    Test add new link object to the database.
    """
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    # Add data
    response = test_client.post(LINKS_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data.get("url") == payload.get("url")
    assert response_data.get("added_by") == payload.get("added_by")
    assert response_data.get("_id")
    assert response_data.get("date_added")


def test_add_link_that_already_exists(test_client):
    """
    Test add new link object with given url that already exists.
    """
    # Add data
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    response = test_client.post(LINKS_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(LINKS_URL, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_check_url_exists(test_client):
    """
    Test check that url exists in the databse.
    """
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    # Add data
    response = test_client.post(LINKS_URL, json=payload)
    # Check exists
    url = CHECK_EXISTS_URL + '?url=https://example.com'
    response = test_client.get(url)
    assert response.status_code == 200


def test_check_url_not_exists(test_client):
    """
    Test check that url exists in the databse.
    """
    # Check exists
    url = CHECK_EXISTS_URL + '?url=https://example.com'
    response = test_client.get(url)
    assert response.status_code == 404


def test_get_links_with_empty_database(test_client):
    """
    Test get links from empty database.
    """
    response = test_client.get(LINKS_URL)
    assert response.status_code == 200
    assert response.json() == []


def test_get_links(test_client):
    """
    Test get links from database.
    """
    # Add some data
    data = []
    for i in range(30):
        res = test_client.post(
            LINKS_URL,
            json={'url': f'https://example{i}.com', 'added_by': 'Someone'}
        )
        data.append(res.json())

    response = test_client.get(LINKS_URL)
    assert response.status_code == 200
    for index, obj in enumerate(response.json()):
        assert obj == data[index]


def test_get_link(test_client):
    """
    Test get link object from database.
    """
    # Add data
    payload = {
        "url": "https://example.com",
        "added_by": "Someone"
    }
    res = test_client.post(LINKS_URL, json=payload)
    res_data = res.json()

    url = LINKS_URL + f"{res_data['_id']}"
    response = test_client.get(url)
    assert response.status_code == 200
    assert response.json() == res_data


def test_get_link_that_not_exists(test_client):
    """
    Test get link object that now exists from database.
    """
    url = LINKS_URL + "test_id"
    response = test_client.get(url)
    assert response.status_code == 404
