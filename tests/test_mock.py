# test_mock.py
from config.config_loader import ConfigLoader
import requests


def test_mocked_api():
    # Initialise ConfigLoader to fetch the base URL(s) from config.yaml dynamically
    config_loader = ConfigLoader()
    wiremock_url = config_loader.get('wiremock_url')

    # Make a GET request to the mocked API
    response = requests.get(f"{wiremock_url}/mocked-user")
    assert response.status_code == 200
    assert response.json()["name"] == "Mock User"
