import pytest
from utils.api_client import APIClient
from config.config_loader import config

@pytest.fixture
def api_client():
    return APIClient()

def test_get_users_page_2_response_verification(api_client):
    """
    Verifies specific elements within the JSON response from /users?page=2.
    """
    try:
        response = api_client.get("/users?page=2")
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

        # Verify specific user data (e.g., the first user)
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
        pytest.fail(f"Test failed: {e}") # fail the test and print the error.