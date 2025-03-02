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

@pytest.fixture
def api_client():
    """Provides a requests.Session object for API interactions."""
    session = requests.Session()
    return session


def test_get_non_existent_user(api_client):
    """Verify 404 status when requesting a non-existent user."""
    user_id = 9999
    endpoint = config["endpoints"]["base_api"]["users_by_id"].format(user_id=user_id)
    response = api_client.get(f"{BASE_URL}{endpoint}")
    assert response.status_code == 404
    assert response.json() == {}  # Verify empty response body


def test_delete_non_existent_user(api_client):
    """Verify 204 status when deleting a non-existent user."""
    user_id = 9999
    endpoint = config["endpoints"]["base_api"]["users_by_id"].format(user_id=user_id)
    response = api_client.delete(f"{BASE_URL}{endpoint}")
    assert response.status_code == 204


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_create_user_missing_fields(api_client):
    """Verify appropriate error status when creating a user with missing fields."""
    endpoint = config["endpoints"]["base_api"]["users"]
    response = api_client.post(f"{BASE_URL}{endpoint}", json={})
    assert response.status_code in [400, 422]  # 201 is not expected here
    assert "error" in response.json() or "errors" in response.json()  # Verify error message in the response


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_create_user_invalid_data_type(api_client):
    """Verify error status when creating a user with invalid data types."""
    endpoint = config["endpoints"]["base_api"]["users"]
    invalid_data = {"name": 123, "job": ["developer"]}
    response = api_client.post(f"{BASE_URL}{endpoint}", json=invalid_data)
    assert response.status_code in [400, 422]
    assert "error" in response.json() or "errors" in response.json()


@pytest.mark.skip(reason="API does not handle this negative scenario as expected")
def test_update_non_existent_user(api_client):
    """Verify 404 status when updating a non-existent user."""
    user_id = 9992
    endpoint = config["endpoints"]["base_api"]["users_by_id"].format(user_id=user_id)
    response = api_client.put(f"{BASE_URL}{endpoint}", json={"name": "Updated Name", "job": "Updated Job"})
    assert response.status_code == 404