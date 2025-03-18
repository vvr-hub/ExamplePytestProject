import requests


def test_mocked_api(requests_mock, config_loader, data_loader):
    """Test the mocked API endpoint using requests_mock."""
    wiremock_url = config_loader.get("wiremock_url")
    mocked_user_endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=2)

    mocked_data = data_loader.get_data("mocked_user")

    requests_mock.get(
        f"{wiremock_url}{mocked_user_endpoint}",
        json=mocked_data,
        status_code=200,
    )

    response = requests.get(f"{wiremock_url}{mocked_user_endpoint}")

    assert response.status_code == 200
    assert response.json()["name"] == mocked_data["name"]
    assert response.json()["id"] == mocked_data["id"]
