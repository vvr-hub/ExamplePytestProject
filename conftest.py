import pytest
from utils.zap_helper import ZAPHelper


@pytest.fixture(scope="session")
def zap():
    """Fixture to initialise OWASP ZAP for API security scanning."""
    zap_instance = ZAPHelper()

    # Start API Scan Automatically When Fixture is Used
    zap_instance.start_api_scan()

    yield zap_instance

    # Generate Report After Tests Complete
    zap_instance.generate_report()
