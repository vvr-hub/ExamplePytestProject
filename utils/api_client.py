import requests
from config.config_loader import ConfigLoader


class APIClient:
    def __init__(self):
        # Initialise the config loader and retrieve configuration values
        config_loader = ConfigLoader()  # Initialise ConfigLoader instance
        self.base_url = config_loader.get('base_url')  # Fetch base_url from config
        self.auth_token = config_loader.get('auth_token')  # Fetch auth_token from config
        self.headers = {"Authorization": f"Bearer {self.auth_token}"}  # Set authorization headers

    def get(self, endpoint, params=None):
        # Send a GET request to the API
        response = requests.get(f"{self.base_url}{endpoint}", params=params, headers=self.headers)
        return response

    def post(self, endpoint, data):
        # Send a POST request to the API
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=self.headers)
        return response

    def put(self, endpoint, data):
        # Send a PUT request to the API
        response = requests.put(f"{self.base_url}{endpoint}", json=data, headers=self.headers)
        return response

    def delete(self, endpoint):
        # Send a DELETE request to the API
        response = requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)
        return response
