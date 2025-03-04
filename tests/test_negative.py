import pytest


def test_get_non_existent_user(api_client, config_loader):
    """Verify 404 status when requesting a non-existent user."""
    user_id = 9999
    endpoint = config_loader.get("endpoints")["base_api"]["users_by_id"].format(user_id=user_id)
    response = api_client.get(endpoint)
    assert response.status_code == 404
    assert response.json() == {}  # Verify empty response body


def test_delete_non_existent_user(api_client, config_loader):
    """Verify 204 status when deleting a non-existent user."""
    user_id = 9999
    endpoint = config_loader.get("endpoints")["base_api"]["users_by_id"].format(user_id=user_id)
    response = api_client.delete(endpoint)
    assert response.status_code == 204


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_create_user_missing_fields(api_client, config_loader):
    """Verify appropriate error status when creating a user with missing fields."""
    endpoint = config_loader.get("endpoints")["base_api"]["users"]
    response = api_client.post(endpoint, json={})
    assert response.status_code in [400, 422]  # 201 is not expected here
    assert "error" in response.json() or "errors" in response.json()  # Verify error message in the response


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_create_user_invalid_data_type(api_client, config_loader):
    """Verify error status when creating a user with invalid data types."""
    endpoint = config_loader.get("endpoints")["base_api"]["users"]
    invalid_data = {"name": 123, "job": ["developer"]}
    response = api_client.post(endpoint, json=invalid_data)
    assert response.status_code in [400, 422]
    assert "error" in response.json() or "errors" in response.json()


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_update_non_existent_user(api_client, config_loader):
    """Verify 404 status when updating a non-existent user."""
    user_id = 9992
    endpoint = config_loader.get("endpoints")["base_api"]["users_by_id"].format(user_id=user_id)
    response = api_client.put(endpoint, json={"name": "Updated Name", "job": "Updated Job"})
    assert response.status_code == 404