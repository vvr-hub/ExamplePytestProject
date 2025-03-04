import yaml
import os


class ConfigLoader:
    def __init__(self, config_file="config/config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        # Load the YAML configuration file
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)

        # Replace environment variable references with actual values
        for key, value in config.items():
            if isinstance(value, str) and "${" in value:
                config[key] = self.resolve_env_variables(value)

        return config

    def resolve_env_variables(self, value):
        # Look for environment variables wrapped in `${}`
        start = value.find("${") + 2
        end = value.find("}", start)
        env_var = value[start:end]

        # Get the environment variable value, or return the original if not found
        env_value = os.getenv(env_var, f"${{{env_var}}}")
        return value.replace(f"${{{env_var}}}", env_value)

    def get(self, key):
        # Retrieve a value from the loaded config
        return self.config.get(key)

    def get_base_url(self):
        # Retrieve the base_url from the loaded config
        return self.get('base_url')