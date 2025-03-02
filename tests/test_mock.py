# test_mock.py
from config.config_loader import ConfigLoader
import requests

def test_mocked_api():
    # Initialize the config loader and fetch the mock base URL
    config_loader = ConfigLoader()
    wiremock_url = config_loader.get('wiremock_url')  # Fetch the mock base URL from the config

    # Make a GET request to the mocked API
    response = requests.get(f"{wiremock_url}/mocked-user")  # Use wiremock_url from config
    assert response.status_code == 200
    assert response.json()["name"] == "Mock User"
