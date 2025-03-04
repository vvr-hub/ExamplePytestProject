from config.config_loader import ConfigLoader
import subprocess
import requests
import pytest
import time
import os
import json

config_loader = ConfigLoader()
BASE_URL = config_loader.get('base_url')
WIREMOCK_URL = config_loader.get('wiremock_url')

@pytest.fixture
def api_client(requests_mock):
    def _api_client():
        return requests_mock.session()

    _api_client.base_url = BASE_URL
    return _api_client

@pytest.fixture
def wiremock_client(requests_mock):
    def _wiremock_client():
        return requests_mock.session()

    _wiremock_client.base_url = WIREMOCK_URL
    return _wiremock_client

def _setup_wiremock():
    """Ensures WireMock is running and configures stubs."""
    try:
        subprocess.run(["docker", "info"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        pytest.exit("Docker is not running. Please start Docker and retry.")

    def is_wiremock_running():
        try:
            response = requests.get(f"{WIREMOCK_URL}/__admin", allow_redirects=False)
            return response.status_code in (200, 302)
        except requests.exceptions.ConnectionError:
            return False

    if not is_wiremock_running():
        print("WireMock is not running. Starting WireMock in Docker...")
        project_root = os.getcwd()
        wiremock_volume_path = os.path.join(project_root, "wiremock")
        subprocess.run(
            [
                "docker", "run", "-d", "--rm", "--name", "wiremock",
                "-p", "8080:8080", "-v", f"{wiremock_volume_path}:/home/wiremock",
                "wiremock/wiremock"
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(5)

    for _ in range(10):
        if is_wiremock_running():
            break
        time.sleep(1)
    else:
        pytest.exit("WireMock did not start in time.")

    with open("mocks/wiremock_stubs.json", "r") as f:
        stubs = json.load(f)

    for stub in stubs:
        response = requests.post(f"{WIREMOCK_URL}/__admin/mappings", json=stub)
        if response.status_code not in [200, 201]:
            pytest.exit(f"Failed to configure WireMock stub: {response.text}")

def pytest_sessionstart(session):
    """Called before the start of the test session."""
    _setup_wiremock()