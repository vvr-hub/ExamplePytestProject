import requests

def test_mocked_api():
    response = requests.get("http://localhost:8080/mocked-user")
    assert response.status_code == 200
    assert response.json()["name"] == "Mock User"
