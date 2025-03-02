import pytest
import yaml
from pathlib import Path
from utils.api_client import APIClient
import os

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
    return APIClient()


@pytest.mark.parametrize("page", [1, 2, 3])
def test_get_users_pages(api_client, page):
    endpoint = config["endpoints"]["base_api"]["users_page"].format(page=page)
    response = api_client.get(f"{endpoint}")
    assert response.status_code == 200
    assert response.ok
    assert "data" in response.json()


def test_get_users_page_2_response_verification(api_client):
    """
    Verifies specific elements within the JSON response from /users?page=2.
    """
    try:
        endpoint = config["endpoints"]["base_api"]["users_page"].format(page=2)
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
        first_user = data[0]
        assert first_user["id"] == 7
        assert first_user["email"] == "michael.lawson@reqres.in"
        assert first_user["first_name"] == "Michael"
        assert first_user["last_name"] == "Lawson"
        assert "https://reqres.in/img/faces/7-image.jpg" in first_user["avatar"]

        # Verify support data
        support = json_response["support"]
        assert "https://contentcaddy.io" in support["url"]
        assert "Tired of writing endless social media content?" in support["text"]

    except Exception as e:
        pytest.fail(f"Test failed: {e}")  # fail the test and print the error.


def test_create_and_delete_user(api_client):
    data = {"name": "John Doe", "job": "QA Engineer"}

    # Create user
    endpoint_create = config["endpoints"]["base_api"]["users"]
    create_response = api_client.post(f"{endpoint_create}", data)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Delete user
    endpoint_delete = config["endpoints"]["base_api"]["users_by_id"].format(user_id=user_id)
    delete_response = api_client.delete(f"{endpoint_delete}")
    assert delete_response.status_code == 204

    # Verify that the user is actually deleted (example, by trying to GET it)
    endpoint_verify = config["endpoints"]["base_api"]["users_by_id"].format(user_id=user_id)
    verify_delete_response = api_client.get(f"{endpoint_verify}")
    assert verify_delete_response.status_code == 404, "User should be deleted"