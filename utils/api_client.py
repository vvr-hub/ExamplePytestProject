import requests
from config.config_loader import config

class APIClient:
    def __init__(self):
        self.base_url = config["base_url"]
        self.headers = {"Authorization": f"Bearer {config['auth_token']}"}

    def get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}{endpoint}", params=params, headers=self.headers)
        return response

    def post(self, endpoint, data):
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=self.headers)
        return response

    def put(self, endpoint, data):
        response = requests.put(f"{self.base_url}{endpoint}", json=data, headers=self.headers)
        return response

    def delete(self, endpoint):
        response = requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)
        return response
