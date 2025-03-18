import pytest


@pytest.mark.parametrize("page", [1, 2, 3])
def test_get_users_pages(api_client, page, config_loader):
    """Test retrieving users with pagination."""
    endpoint = config_loader.get_api_endpoints("users_page").format(page=page)

    response = api_client.get(endpoint)

    assert response.status_code == 200
    assert response.json()["page"] == page


def test_get_users_page_2_response_verification(api_client, config_loader, data_loader):
    """Verifies specific elements within the JSON response from /users?page=2."""
    endpoint = config_loader.get_api_endpoints("users_page").format(page=2)

    response = api_client.get(endpoint)
    response.raise_for_status()

    json_response = response.json()

    assert json_response["page"] == 2
    assert json_response["per_page"] == 6
    assert json_response["total"] == 12
    assert json_response["total_pages"] == 2


def test_create_and_delete_user(api_client, config_loader, data_loader):
    """Test user creation and deletion."""
    create_endpoint = config_loader.get_api_endpoints("create_user")
    user_data = data_loader.get_data("users", "valid_user")

    create_response = api_client.post(create_endpoint, data=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    delete_endpoint = config_loader.get_api_endpoints("delete_user").format(user_id=user_id)
    delete_response = api_client.delete(delete_endpoint)

    assert delete_response.status_code == 204
