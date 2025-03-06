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
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML in {data_file_path}: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while loading data: {e}")

    def get_data(self, section, key=None):
        try:
            section_data = self.data.get(section)
            if section_data is None:
                raise KeyError(f"Section '{section}' not found in data.")

            if key:
                value = section_data.get(key)
                if value is None:
                    raise KeyError(f"Key '{key}' not found in section '{section}'.")
                return value
            return section_data
        except KeyError as e:
            raise e  # Re-raise the KeyError to maintain its specific type
        except AttributeError:
            raise AttributeError("Data has not been loaded. Check the DataLoader initialization.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while getting data: {e}")