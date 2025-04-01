# tests/conftest.py
from config.config_loader import ConfigLoader
import subprocess
import requests
import pytest
import time
import logging
import os
import json
from utils.api_client import APIClient
from data.data_loader import DataLoader


@pytest.fixture(scope="session")
def config_loader():
    try:
        return ConfigLoader()
    except Exception as e:
        pytest.exit(f"Failed to load configuration: {e}")


@pytest.fixture(scope="session")
def data_loader():
    try:
        return DataLoader()
    except Exception as e:
        pytest.exit(f"Failed to load data: {e}")


@pytest.fixture(scope="session")
def base_url(config_loader):
    try:
        return config_loader.get_base_url()
    except Exception as e:
        pytest.exit(f"Failed to get base URL: {e}")


@pytest.fixture(scope="session")
def wiremock_url(config_loader):
    try:
        return config_loader.get_wiremock_url()
    except Exception as e:
        pytest.exit(f"Failed to get WireMock URL: {e}")


@pytest.fixture(scope="session")
def api_client(base_url, config_loader): # Pytest automatically resolves these parameters by looking for other fixtures with these names. (fixture dependency)
    try:
        if not base_url:
            raise ValueError("⚠️ ERROR: Base URL is None, cannot create API Client!")

        logging.info(f"🌍 Using Base URL: {base_url}")

        # 🔍 Debug: Log config contents
        logging.info(f"🛠️ Config Contents: {config_loader.config}")

        return APIClient(base_url, config_loader)
    except Exception as e:
        pytest.exit(f"Failed to create API client: {e}")


@pytest.fixture
def wiremock_client(wiremock_url):
    try:
        session = requests.Session()
        session.base_url = wiremock_url
        return session
    except Exception as e:
        pytest.exit(f"Failed to create WireMock client session: {e}")


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
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError in is_wiremock_running: {e}")
            return False

    if not is_wiremock_running():
        print("WireMock is not running. Starting WireMock in Docker...")
        project_root = os.getcwd()
        wiremock_volume_path = os.path.join(project_root, "wiremock")
        try:
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
        except subprocess.CalledProcessError as e:
            pytest.exit(f"Failed to start WireMock in Docker: {e}")

        for _ in range(10):
            if is_wiremock_running():
                break
            time.sleep(1)
        else:
            pytest.exit("WireMock did not start in time.")

    try:
        with open("mocks/wiremock_stubs.json", "r") as f:
            stubs = json.load(f)

        for stub in stubs:
            response = requests.post(f"{wiremock_url}/__admin/mappings", json=stub)
            if response.status_code not in [200, 201]:
                pytest.exit(f"Failed to configure WireMock stub: {response.text}")
    except (FileNotFoundError, json.JSONDecodeError, requests.exceptions.RequestException) as e:
        pytest.exit(f"Failed to configure WireMock stubs: {e}")


def pytest_sessionstart(session):
    """This Pytest Hook is called before the start of the test session."""
    try:
        config_loader_instance = ConfigLoader()
        wiremock_url_instance = config_loader_instance.get_wiremock_url()
        _setup_wiremock(wiremock_url_instance)
    except Exception as e:
        pytest.exit(f"Session start failed: {e}")
