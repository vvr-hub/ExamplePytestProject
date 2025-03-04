import requests


class APIClient:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = requests.Session()

    def post(self, endpoint, data=None, headers=None):  # Added headers parameter
        url = f"{self.base_url}{endpoint}"
        default_headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        if headers:
            default_headers.update(headers)  # Merge custom headers if provided
        return self.session.post(url, json=data, headers=default_headers)

    def get(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        if headers:
            return self.session.get(url, headers=headers)
        return self.session.get(url)

    def put(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        return self.session.put(url, json=data, headers=headers)

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        return self.session.delete(url, headers=headers)
