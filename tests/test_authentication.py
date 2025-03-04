import pytest


def test_successful_login(api_client, config_loader, data_loader):
    """Test login with valid credentials."""
    login_endpoint = config_loader.get("endpoints")["base_api"]["login"]
    user_data = data_loader.get_data("auth", "valid_credentials")
    response = api_client.post(login_endpoint, data=user_data)
    assert response.status_code == 200
    assert "token" in response.json()


def test_failed_login(api_client, config_loader, data_loader):
    """Test login with invalid credentials."""
    login_endpoint = config_loader.get("endpoints")["base_api"]["login"]
    user_data = data_loader.get_data("auth", "invalid_credentials")
    response = api_client.post(login_endpoint, data=user_data)
    assert response.status_code == 400
    assert "error" in response.json()


def test_access_protected_route(api_client, config_loader, data_loader):
    """Test accessing a protected route with a valid token."""
    login_endpoint = config_loader.get("endpoints")["base_api"]["login"]
    user_data = data_loader.get_data("auth", "valid_credentials")
    login_response = api_client.post(login_endpoint, data=user_data)
    token = login_response.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    users_by_id_endpoint = config_loader.get("endpoints")["base_api"]["users_by_id"].format(user_id=2)
    response = api_client.get(users_by_id_endpoint, headers=headers)
    assert response.status_code == 200


@pytest.mark.skip(reason="Unable to test API denying access when token is invalid. It has no protected endpoints")
def test_access_protected_route_invalid_token(api_client, config_loader, data_loader):
    """Test accessing a protected route with an invalid token."""
    invalid_token = data_loader.get_data("auth", "invalid_token")
    headers = {"Authorization": f"Bearer {invalid_token}"}
    admin_dashboard_endpoint = config_loader.get("endpoints")["wiremock"]["admin_dashboard"]
    response = api_client.get(admin_dashboard_endpoint, headers=headers)
    assert response.status_code == 401


@pytest.mark.skip(reason="Unable to test API denying access when token is not provided. It has no protected endpoints")
def test_access_protected_route_no_token(api_client, config_loader, data_loader):
    """Test accessing a protected route without a token."""
    login_endpoint = config_loader.get("endpoints")["base_api"]["login"]
    user_data = data_loader.get_data("auth", "valid_credentials")
    login_response = api_client.post(login_endpoint, data=user_data)
    token = login_response.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    admin_dashboard_endpoint = config_loader.get("endpoints")["wiremock"]["admin_dashboard"]
    unprotected_response = api_client.get(admin_dashboard_endpoint)  # No auth header present
    assert unprotected_response.status_code in [401,
                                                403], "Protected route should be inaccessible without authentication."


def test_mock_access_protected_route_with_invalid_token(wiremock_client, config_loader, wiremock_url, requests_mock,
                                                        data_loader):
    """Test accessing a protected route with an invalid token."""
    invalid_token = data_loader.get_data("auth", "invalid_token")
    headers = {"Authorization": f"Bearer {invalid_token}"}
    admin_dashboard_endpoint = config_loader.get("endpoints")["wiremock"]["admin_dashboard"]
    full_url = f"{wiremock_url}{admin_dashboard_endpoint}"
    requests_mock.get(full_url, status_code=401, json={"error": "Unauthorized"})
    response = wiremock_client.get(full_url, headers=headers)
    assert response.status_code == 401
    assert "error" in response.json()


def test_mock_access_protected_route_no_token(wiremock_client, config_loader, wiremock_url, requests_mock):
    """Test accessing a protected route without a token."""
    admin_dashboard_endpoint = config_loader.get("endpoints")["wiremock"]["admin_dashboard"]
    full_url = f"{wiremock_url}{admin_dashboard_endpoint}"
    requests_mock.get(full_url, status_code=401, json={"error": "Unauthorized"})
    response = wiremock_client.get(full_url)  # No auth header
    assert response.status_code == 401
    assert "error" in response.json()
