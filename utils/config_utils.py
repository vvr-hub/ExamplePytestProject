import yaml
from pathlib import Path


def load_config():
    """Loads the configuration from config.yaml."""
    try:
        root_dir = Path(__file__).resolve().parent.parent
        config_path = root_dir / 'config' / 'config.yaml'
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: config.yaml not found at {config_path}")
        raise
