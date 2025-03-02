import yaml
import os

def load_config():
    config_path = "config/config.yaml"  # Store path in a variable for clarity

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML in {config_path}: {e}")  # More specific exception
    except Exception as e: # Catch any other potential errors
        raise Exception(f"An unexpected error occurred while loading config: {e}")

# Make config a global variable
try:
    config = load_config()
except (FileNotFoundError, ValueError, Exception) as e:  # Catch specific exceptions
    print(f"Error loading configuration: {e}") # Print the error
    exit(1)  # Exit the program with a non-zero code to indicate an error

    # Handle the error appropriately in alternative ways. Here are some examples:
    # 1. Use default config values or other fallback mechanisms
    # config = {"base_url": "default_url", ...}
    # 2. Reraise the exception if you want calling function to handle it
    # raise # Re-raise the caught exception

if 'base_url' in config: # Check if config was loaded before using it
    print(f"Base URL: {config['base_url']}")
else:
    print("Configuration not loaded. Using defaults or exiting...")