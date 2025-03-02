import requests
import yaml
from pathlib import Path


# Load config from the root directory
def load_config():
    try:
        # Get the root directory
        root_dir = Path(__file__).resolve().parent.parent
        # Construct the path to config.yaml (inside the config folder)
        config_path = root_dir / 'config' / 'config.yaml'

        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: config.yaml not found at {config_path}")
        raise


config = load_config()


def test_mocked_api():
    """Test the mocked API endpoint."""
    wiremock_url = config["wiremock_url"]
    mocked_user_endpoint = config["endpoints"]["wiremock"]["mocked_user"]

    response = requests.get(f"{wiremock_url}{mocked_user_endpoint}")
    assert response.status_code == 200
    assert response.json()["name"] == "Mock User"
