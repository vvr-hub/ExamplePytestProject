import pytest


def test_successful_login(api_client, config_loader, data_loader):
    """Test successful login and token retrieval."""
    endpoint = config_loader.get_api_endpoints("login")
    payload = data_loader.get_data("auth", "valid_credentials")

    response = api_client.post(endpoint, data=payload)

    assert response.status_code == 200
    assert "token" in response.json()


def test_failed_login(api_client, config_loader, data_loader):
    """Test login failure with incorrect credentials."""
    endpoint = config_loader.get_api_endpoints("login")
    payload = data_loader.get_data("auth", "invalid_credentials")

    response = api_client.post(endpoint, data=payload)

    assert response.status_code == 400 or response.status_code == 401


def test_access_protected_route(api_client, config_loader, data_loader):
    """Test accessing a protected route with a valid token."""
    login_endpoint = config_loader.get_api_endpoints("login")
    user_data = data_loader.get_data("auth", "valid_credentials")

    login_response = api_client.post(login_endpoint, data=user_data)
    token = login_response.json().get("token")

    assert token, "Failed to retrieve authentication token"

    headers = {"Authorization": f"Bearer {token}"}
    users_by_id_endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=2)

    response = api_client.get(users_by_id_endpoint, headers=headers)

    assert response.status_code == 200


@pytest.mark.skip(reason="API does not implement authentication")
def test_access_protected_route_invalid_token(api_client, config_loader):
    """Test accessing a protected route with an invalid token."""
    users_by_id_endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=2)
    headers = {"Authorization": "Bearer invalid_token"}

    response = api_client.get(users_by_id_endpoint, headers=headers)

    assert response.status_code == 403 or response.status_code == 401


@pytest.mark.skip(reason="API does not implement authentication")
def test_access_protected_route_no_token(api_client, config_loader):
    """Test accessing a protected route without a token."""
    users_by_id_endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=2)

    response = api_client.get(users_by_id_endpoint)

    assert response.status_code == 403 or response.status_code == 401
