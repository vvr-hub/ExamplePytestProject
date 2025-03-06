# utils/api_client.py
import requests


class APIClient:
    def __init__(self, base_url, config_loader):
        self.base_url = base_url
        self.config_loader = config_loader
        self.session = requests.Session()
        self.auth_token = self._get_auth_token()

    def _get_auth_token(self):
        try:
            auth_endpoint = self.config_loader.get("endpoints")["auth"]["login"]
            username = self.config_loader.get("auth_credentials")["username"]
            password = self.config_loader.get("auth_credentials")["password"]

            response = self.session.post(f"{self.base_url}{auth_endpoint}",
                                         json={"username": username, "password": password})
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()["token"]
        except (KeyError, requests.exceptions.RequestException) as e:
            print(f"Authentication failed: {e}")
            return None

    def post(self, endpoint, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        default_headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        if headers:
            default_headers.update(headers)
        return self.session.post(url, json=data, headers=default_headers)

    def get(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        default_headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        if headers:
            default_headers.update(headers)
        return self.session.get(url, headers=default_headers)

    def put(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        return self.session.put(url, json=data, headers=headers)

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        return self.session.delete(url, headers=headers)
