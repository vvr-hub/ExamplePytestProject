import pytest
from utils.api_client import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.parametrize("page", [1, 2, 3])
def test_get_users_pages(api_client, page):
    response = api_client.get(f"/users?page={page}")
    assert response.status_code == 200
    assert response.ok
    assert "data" in response.json()