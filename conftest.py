import pytest
import os
from utils.zap_helper import ZAPHelper
from config.config_loader import ConfigLoader

# Load configuration
config = ConfigLoader()

# Get values from config.yaml
zap_url = config.get("zap_url") or "http://localhost:8080"
base_url = config.get_base_url()
auth_token = config.get_auth_token()


@pytest.fixture(scope="session")
def zap():
    """Fixture to initialise OWASP ZAP for security scanning."""
    zap_instance = ZAPHelper()
    yield zap_instance
    zap_instance.generate_report()
