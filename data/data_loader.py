import yaml
import os

class DataLoader:
    def __init__(self, environment=None):
        if environment is None:
            environment = os.getenv("TEST_ENV", "qa")  # Default to 'qa'
        self.environment = environment
        self.data = self._load_data()

    def _load_data(self):
        data_file_path = os.path.join("data", f"{self.environment}.yaml")
        try:
            with open(data_file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {data_file_path}")

    def get_data(self, section, key=None):
        section_data = self.data.get(section)
        if key:
            return section_data.get(key)
        return section_data