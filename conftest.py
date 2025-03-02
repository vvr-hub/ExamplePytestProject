# conftest.py (in the root directory)

import yaml
import pytest


def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture
def api_client(config, requests_mock):
    base_url = config["base_url"]

    def _api_client():
        return requests_mock.session()

    _api_client.base_url = base_url
    return _api_client


@pytest.fixture
def wiremock_client(config, requests_mock):
    wiremock_base_url = config["wiremock_base_url"]

    def _wiremock_client():
        return requests_mock.session()

    _wiremock_client.base_url = wiremock_base_url
    return _wiremock_client
