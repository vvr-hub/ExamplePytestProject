import requests
from config import config

class Auth:
    @staticmethod
    def get_token():
        response = requests.post(f"{config['base_url']}/auth", json={"username": "admin", "password": "password"})
        return response.json()["token"] if response.status_code == 200 else None
