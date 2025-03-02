import requests
from config.config_loader import ConfigLoader

# Initialise ConfigLoader to fetch the base URL(s) from config.yaml dynamically
config_loader = ConfigLoader()
BASE_URL = config_loader.get('base_url')


class Auth:
    @staticmethod
    def get_token():
        response = requests.post(f"{'BASE_URL'}/auth", json={"username": "admin", "password": "password"})
        return response.json()["token"] if response.status_code == 200 else None
