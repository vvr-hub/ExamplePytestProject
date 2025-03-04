import requests
from config.config_loader import ConfigLoader

config_loader = ConfigLoader()

def test_mocked_api(requests_mock, data_loader):
    """Test the mocked API endpoint using requests_mock."""
    wiremock_url = config_loader.get("wiremock_url")
    mocked_user_endpoint = config_loader.get_endpoints("wiremock", "mocked_user")
    full_url = f"{wiremock_url}{mocked_user_endpoint}"

    # Define the mock behavior
    mocked_data = data_loader.get_data("mocked_user")
    requests_mock.get(
        full_url,
        json=mocked_data,
        status_code=200,
    )

    response = requests.get(full_url)
    assert response.status_code == 200
    assert response.json()["name"] == mocked_data["name"]
    assert response.json()["id"] == mocked_data["id"]