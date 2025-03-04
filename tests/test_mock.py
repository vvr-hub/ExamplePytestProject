import requests
from utils.config_utils import load_config

config = load_config()

def test_mocked_api(requests_mock):
    """Test the mocked API endpoint using requests_mock."""
    wiremock_url = config["wiremock_url"]
    mocked_user_endpoint = config["endpoints"]["wiremock"]["mocked_user"]
    full_url = f"{wiremock_url}{mocked_user_endpoint}"

    # Define the mock behavior
    requests_mock.get(
        full_url,
        json={"name": "Mock User", "id": 123},  # Example JSON response
        status_code=200,
    )

    response = requests.get(full_url)
    assert response.status_code == 200
    assert response.json()["name"] == "Mock User"
    assert response.json()["id"] == 123 #adding additional assertion to ensure mock is working.