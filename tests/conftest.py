from config.config_loader import ConfigLoader
import subprocess
import requests
import pytest
import time
import os

# Use ConfigLoader to fetch base_url and wiremock_url dynamically
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


@pytest.fixture(scope="session", autouse=True)
def setup_wiremock():
    """Ensures WireMock is running and configures stubs before tests start."""

    def is_wiremock_running():
        try:
            response = requests.get(f"{WIREMOCK_URL}/__admin", allow_redirects=False)
            return response.status_code in (200, 302)
        except requests.exceptions.ConnectionError:
            return False

    def is_docker_running():
        """Check if Docker daemon is running."""
        try:
            subprocess.run(["docker", "info"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    if not is_docker_running():
        pytest.exit("Docker is not running. Please start Docker and retry.")

    if not is_wiremock_running():
        print("WireMock is not running. Starting WireMock in Docker...")
        try:
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
            time.sleep(5)  # Wait for WireMock to be ready
        except subprocess.CalledProcessError as e:
            pytest.exit(f"Failed to start WireMock: {e.stderr.decode()}")

    # Wait until WireMock is available
    for _ in range(10):
        if is_wiremock_running():
            break
        time.sleep(1)
    else:
        pytest.exit("WireMock did not start in time.")

    # Setup WireMock stubs
    setup_stub()


def setup_stub():
    """Sets up WireMock stubs for testing."""
    stubs = [
        {
            "request": {"method": "GET", "url": "/mocked-user"},
            "response": {
                "status": 200,
                "body": '{"id": 1, "name": "Mock User"}',
                "headers": {"Content-Type": "application/json"}
            }
        },
        {
            "request": {
                "method": "GET",
                "url": "/admin/dashboard",
                "headers": {
                    "Authorization": {"matches": "Bearer QpwL5tke4Pnpja7X4"}
                }
            },
            "response": {
                "status": 200,
                "body": '{ "message": "Welcome to Admin Dashboard" }',
                "headers": {"Content-Type": "application/json"}
            }
        },
        {
            "request": {"method": "GET", "url": "/admin/dashboard"},
            "response": {
                "status": 401,
                "body": '{ "error": "Unauthorized access" }',
                "headers": {"Content-Type": "application/json"}
            }
        }
    ]

    for stub in stubs:
        response = requests.post(f"{WIREMOCK_URL}/__admin/mappings", json=stub)
        if response.status_code not in [200, 201]:
            pytest.exit(f"Failed to configure WireMock stub: {response.text}")
