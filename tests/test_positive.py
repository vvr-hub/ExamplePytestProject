import pytest

@pytest.mark.parametrize("page", [1, 2, 3])
def test_get_users_pages(api_client, page, config_loader):
    endpoint = config_loader.get("endpoints")["base_api"]["users_page"].format(page=page)
    response = api_client.get(f"{endpoint}")
    assert response.status_code == 200
    assert response.ok
    assert "data" in response.json()

def test_get_users_page_2_response_verification(api_client, config_loader, data_loader):
    """
    Verifies specific elements within the JSON response from /users?page=2.
    """
    try:
        endpoint = config_loader.get("endpoints")["base_api"]["users_page"].format(page=2)
        response = api_client.get(f"{endpoint}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        json_response = response.json()

        # Verify top-level elements
        assert json_response["page"] == 2
        assert json_response["per_page"] == 6
        assert json_response["total"] == 12
        assert json_response["total_pages"] == 2

        # Verify data array
        data = json_response["data"]
        assert isinstance(data, list)
        assert len(data) == 6

        # Verify specific user data (for example, the first user)
        first_user_data = data_loader.get_data("users", "first_page_user")
        first_user = data[0]
        assert first_user["id"] == first_user_data["id"]
        assert first_user["email"] == first_user_data["email"]
        assert first_user["first_name"] == first_user_data["first_name"]
        assert first_user["last_name"] == first_user_data["last_name"]
        assert first_user_data["avatar"] in first_user["avatar"]

        # Verify support data
        support_data = data_loader.get_data("users", "support")
        support = json_response["support"]
        assert support_data["url"] in support["url"]
        assert support_data["text"] in support["text"]

    except Exception as e:
        pytest.fail(f"Test failed: {e}")  # fail the test and print the error.

def test_create_and_delete_user(api_client, config_loader, data_loader):
    user_data = data_loader.get_data("users", "valid_user")

    # Create user
    endpoint_create = config_loader.get("endpoints")["base_api"]["users"]
    create_response = api_client.post(f"{endpoint_create}", data=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Delete user
    endpoint_delete = config_loader.get("endpoints")["base_api"]["users_by_id"].format(user_id=user_id)
    delete_response = api_client.delete(f"{endpoint_delete}")
    assert delete_response.status_code == 204

    # Verify that the user is actually deleted (example, by trying to GET it)
    endpoint_verify = config_loader.get("endpoints")["base_api"]["users_by_id"].format(user_id=user_id)
    verify_delete_response = api_client.get(f"{endpoint_verify}")
    assert verify_delete_response.status_code == 404, "User should be deleted"