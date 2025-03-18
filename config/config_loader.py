import yaml
import os
import logging


class ConfigLoader:
    def __init__(self, config_file="config/config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        self.environment = os.getenv("TEST_ENV", "qa")  # Default to 'qa'

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML in {self.config_file}: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error while loading config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_base_url(self):
        base_urls = self.get('base_urls', {})
        env_base_url = base_urls.get(self.environment)
        if not env_base_url:
            raise ValueError(f"⚠️ ERROR: No base URL found for environment '{self.environment}' in config.yaml!")
        return env_base_url

    def get_wiremock_url(self):
        return self.get('wiremock_url')

    def get_api_endpoints(self, endpoint_name):
        """Fetches an API endpoint from config."""
        api_endpoints = self.get("api_endpoints", [])
        for ep in api_endpoints:
            if endpoint_name == ep.get("name"):
                return ep.get("url")
        raise KeyError(f"⚠️ Endpoint '{endpoint_name}' not found in API endpoints config.")

    def get_websocket_url(self):
        websocket_url = self.get("websocket_url")
        if not websocket_url:
            raise ValueError("⚠️ WebSocket URL not found in config.")
        return websocket_url
