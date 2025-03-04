from config.config_loader import ConfigLoader
import subprocess
import requests
import pytest
import time
import os
import json
from utils.api_client import APIClient

@pytest.fixture(scope="session")
def config_loader():
    return ConfigLoader()

@pytest.fixture(scope="session")
def base_url(config_loader):
    return config_loader.get_base_url()

@pytest.fixture(scope="session")
def wiremock_url(config_loader):
    return config_loader.get('wiremock_url')

@pytest.fixture(scope="session")
def api_client(base_url, config_loader):
    return APIClient(base_url, config_loader.get('auth_token'))

@pytest.fixture
def wiremock_client(wiremock_url):
    session = requests.Session()
    session.base_url = wiremock_url
    return session

def _setup_wiremock(wiremock_url):
    """Ensures WireMock is running and configures stubs."""
    try:
        subprocess.run(["docker", "info"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        pytest.exit("Docker is not running. Please start Docker and retry.")

    def is_wiremock_running():
        try:
            response = requests.get(f"{wiremock_url}/__admin", allow_redirects=False)
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
        response = requests.post(f"{wiremock_url}/__admin/mappings", json=stub)
        if response.status_code not in [200, 201]:
            pytest.exit(f"Failed to configure WireMock stub: {response.text}")

def pytest_sessionstart(session):
    """Called before the start of the test session."""
    config_loader_instance = ConfigLoader()
    wiremock_url_instance = config_loader_instance.get('wiremock_url')
    _setup_wiremock(wiremock_url_instance)