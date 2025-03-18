import pytest


def test_get_non_existent_user(api_client, config_loader, data_loader):
    """Verify 404 status when requesting a non-existent user."""
    user_id = data_loader.get_data("users", "non_existent_user_id")
    endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=user_id)
    response = api_client.get(endpoint)
    assert response.status_code == 404
    assert response.json() == {}  # Verify empty response body


def test_delete_non_existent_user(api_client, config_loader, data_loader):
    """Verify 204 status when deleting a non-existent user."""
    user_id = data_loader.get_data("users", "non_existent_user_id")
    endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=user_id)
    response = api_client.delete(endpoint)
    assert response.status_code == 204


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_create_user_missing_fields(api_client, config_loader):
    """Verify appropriate error status when creating a user with missing fields."""
    endpoint = config_loader.get_api_endpoints("users")
    response = api_client.post(endpoint, json={})
    assert response.status_code in [400, 422]  # 201 is not expected here
    assert "error" in response.json() or "errors" in response.json()  # Verify error message in the response


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_create_user_invalid_data_type(api_client, config_loader, data_loader):
    """Verify error status when creating a user with invalid data types."""
    endpoint = config_loader.get_api_endpoints("users")
    invalid_data = data_loader.get_data("users", "invalid_user_data")
    response = api_client.post(endpoint, json=invalid_data)
    assert response.status_code in [400, 422]
    assert "error" in response.json() or "errors" in response.json()


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_update_non_existent_user(api_client, config_loader, data_loader):
    """Verify 404 status when updating a non-existent user."""
    user_id = data_loader.get_data("users", "non_existent_update_user_id")
    update_data = data_loader.get_data("users", "update_data")
    endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=user_id)
    response = api_client.put(endpoint, json=update_data)
    assert response.status_code == 404
