import requests
from utils.config_utils import load_config

config = load_config()


def test_mocked_api():
    """Test the mocked API endpoint."""
    wiremock_url = config["wiremock_url"]
    mocked_user_endpoint = config["endpoints"]["wiremock"]["mocked_user"]

    response = requests.get(f"{wiremock_url}{mocked_user_endpoint}")
    assert response.status_code == 200
    assert response.json()["name"] == "Mock User"
