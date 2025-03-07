# config/config_loader.py

import yaml
import os


class ConfigLoader:
    def __init__(self, config_file="config/config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        self.environment = os.getenv("TEST_ENV", "qa")  # Default to 'qa'

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML in {self.config_file}: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while loading config: {e}")

    def get(self, key):
        try:
            return self.config.get(key)
        except AttributeError:
            raise AttributeError(f"Config has no attribute '{key}'")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting config key '{key}': {e}")

    def get_base_url(self):
        try:
            base_urls = self.get('base_urls')
            return base_urls.get(self.environment)
        except AttributeError:
            raise AttributeError(f"Base URLs for environment '{self.environment}' not found in config.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting base URL: {e}")

    def get_wiremock_url(self):
        try:
            return self.get('wiremock_url')
        except AttributeError:
            raise AttributeError("WireMock URL not found in config.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting WireMock URL: {e}")

    def get_endpoints(self, endpoint_group, endpoint_name):
        try:
            return self.get('endpoints').get(endpoint_group).get(endpoint_name)
        except AttributeError:
            raise AttributeError(f"Endpoint '{endpoint_name}' in group '{endpoint_group}' not found in config.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting endpoint: {e}")

    def get_auth_token(self):
        try:
            return self.get('auth_token')
        except AttributeError:
            raise AttributeError("Auth token not found in config.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting auth token: {e}")

    def get_websocket_url(self):
        try:
            return self.get('websocket_url')
        except AttributeError:
            raise AttributeError("WebSocket URL not found in config.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting WebSocket URL: {e}")
