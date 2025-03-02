import pytest
from utils.api_client import APIClient

client = APIClient()

def test_create_and_delete_user():
    data = {"name": "John Doe", "job": "QA Engineer"}

    create_response = client.post("/users", data)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    # Verify that the user is actually deleted (example, by trying to GET it)
    verify_delete_response = client.get(f"/users/{user_id}")
    assert verify_delete_response.status_code == 404, "User should be deleted"