import yaml
import os


class ConfigLoader:
    def __init__(self, config_file="config/config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        self.environment = os.getenv("TEST_ENV", "qa")  # Default to 'qa'

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def get(self, key):
        return self.config.get(key)

    def get_base_url(self):
        base_urls = self.get('base_urls')
        return base_urls.get(self.environment)

    def get_wiremock_url(self):
        return self.get('wiremock_url')

    def get_endpoints(self, endpoint_group, endpoint_name):
        return self.get('endpoints').get(endpoint_group).get(endpoint_name)

    def get_auth_token(self):
        return self.get('auth_token')
