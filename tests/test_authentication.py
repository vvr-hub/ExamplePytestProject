from config.config_loader import ConfigLoader
import pytest
import requests

# Initialize ConfigLoader to fetch base_url from config.yaml
config_loader = ConfigLoader()
BASE_URL = config_loader.get('base_url')  # Fetch base_url dynamically from config
WIREMOCK_URL = config_loader.get('wiremock_url')


@pytest.fixture
def valid_credentials():
    return {"email": "eve.holt@reqres.in", "password": "cityslicka"}


@pytest.fixture
def invalid_credentials():
    return {"email": "invalid@example.com", "password": "wrongpass"}


@pytest.fixture
def valid_token():
    """Fixture to obtain a valid token for protected route testing."""
    login_response = requests.post(f"{BASE_URL}/login", json={"email": "eve.holt@reqres.in", "password": "cityslicka"})
    assert login_response.status_code == 200, "Failed to obtain valid token"
    return login_response.json().get("token")


def test_successful_login(valid_credentials):
    """Test login with valid credentials."""
    response = requests.post(f"{BASE_URL}/login", json=valid_credentials)
    assert response.status_code == 200
    assert "token" in response.json()


def test_failed_login(invalid_credentials):
    """Test login with invalid credentials."""
    response = requests.post(f"{BASE_URL}/login", json=invalid_credentials)
    assert response.status_code == 400
    assert "error" in response.json()


def test_access_protected_route(valid_token):
    """Test accessing a protected route with a valid token."""
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = requests.get(f"{BASE_URL}/users/2", headers=headers)
    assert response.status_code == 200


@pytest.mark.skip(reason="Unable to test API denying access when token is invalid. It has no protected endpoints")
def test_access_protected_route_invalid_token():
    """Test accessing a protected route with an invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{BASE_URL}/admin/dashboard",
                            headers=headers)  # Assume API contains a protected end-point /admin/dashboard
    assert response.status_code == 401


@pytest.mark.skip(reason="Unable to test API denying access when token is not provided. It has no protected endpoints")
def test_access_protected_route_no_token(valid_token):
    """Test accessing a protected route without a token."""
    headers = {"Authorization": f"Bearer {valid_token}"}
    unprotected_response = requests.get(f"{BASE_URL}/admin/dashboard")  # No auth header present
    assert unprotected_response.status_code in [401,
                                                403], "Protected route should be inaccessible without authentication."


def test_mock_access_protected_route_with_invalid_token():
    """Test accessing a protected route with an invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{WIREMOCK_URL}/admin/dashboard", headers=headers)
    assert response.status_code == 401
    assert "error" in response.json()


def test_mock_access_protected_route_no_token():
    """Test accessing a protected route without a token."""
    response = requests.get(f"{WIREMOCK_URL}/admin/dashboard")  # No auth header
    assert response.status_code == 401
    assert "error" in response.json()

