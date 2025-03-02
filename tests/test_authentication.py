import pytest
import requests
import yaml
from pathlib import Path


# Load config from the root directory
def load_config():
    try:
        # Get the root directory
        root_dir = Path(__file__).resolve().parent.parent
        # Construct the path to config.yaml (inside the config folder)
        config_path = root_dir / 'config' / 'config.yaml'

        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: config.yaml not found at {config_path}")
        raise


config = load_config()

BASE_URL = config["base_url"]
WIREMOCK_URL = config["wiremock_url"]


@pytest.fixture
def valid_credentials():
    return {"email": "eve.holt@reqres.in", "password": "cityslicka"}


@pytest.fixture
def invalid_credentials():
    return {"email": "invalid@example.com", "password": "wrongpass"}


@pytest.fixture
def valid_token():
    """Fixture to obtain a valid token for protected route testing."""
    login_endpoint = config["endpoints"]["base_api"]["login"]
    login_response = requests.post(f"{BASE_URL}{login_endpoint}",
                                   json={"email": "eve.holt@reqres.in", "password": "cityslicka"})
    assert login_response.status_code == 200, "Failed to obtain valid token"
    return login_response.json().get("token")


def test_successful_login(valid_credentials):
    """Test login with valid credentials."""
    login_endpoint = config["endpoints"]["base_api"]["login"]
    response = requests.post(f"{BASE_URL}{login_endpoint}", json=valid_credentials)
    assert response.status_code == 200
    assert "token" in response.json()


def test_failed_login(invalid_credentials):
    """Test login with invalid credentials."""
    login_endpoint = config["endpoints"]["base_api"]["login"]
    response = requests.post(f"{BASE_URL}{login_endpoint}", json=invalid_credentials)
    assert response.status_code == 400
    assert "error" in response.json()


def test_access_protected_route(valid_token):
    """Test accessing a protected route with a valid token."""
    headers = {"Authorization": f"Bearer {valid_token}"}
    users_by_id_endpoint = config["endpoints"]["base_api"]["users_by_id"].format(user_id=2)
    response = requests.get(f"{BASE_URL}{users_by_id_endpoint}", headers=headers)
    assert response.status_code == 200


@pytest.mark.skip(reason="Unable to test API denying access when token is invalid. It has no protected endpoints")
def test_access_protected_route_invalid_token():
    """Test accessing a protected route with an invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    admin_dashboard_endpoint = config["endpoints"]["wiremock"]["admin_dashboard"]
    response = requests.get(f"{BASE_URL}{admin_dashboard_endpoint}", headers=headers)
    assert response.status_code == 401


@pytest.mark.skip(reason="Unable to test API denying access when token is not provided. It has no protected endpoints")
def test_access_protected_route_no_token(valid_token):
    """Test accessing a protected route without a token."""
    headers = {"Authorization": f"Bearer {valid_token}"}
    admin_dashboard_endpoint = config["endpoints"]["wiremock"]["admin_dashboard"]
    unprotected_response = requests.get(f"{BASE_URL}{admin_dashboard_endpoint}")  # No auth header present
    assert unprotected_response.status_code in [401,
                                                403], "Protected route should be inaccessible without authentication."


def test_mock_access_protected_route_with_invalid_token():
    """Test accessing a protected route with an invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    admin_dashboard_endpoint = config["endpoints"]["wiremock"]["admin_dashboard"]
    response = requests.get(f"{WIREMOCK_URL}{admin_dashboard_endpoint}", headers=headers)
    assert response.status_code == 401
    assert "error" in response.json()


def test_mock_access_protected_route_no_token():
    """Test accessing a protected route without a token."""
    admin_dashboard_endpoint = config["endpoints"]["wiremock"]["admin_dashboard"]
    response = requests.get(f"{WIREMOCK_URL}{admin_dashboard_endpoint}")  # No auth header
    assert response.status_code == 401
    assert "error" in response.json()
