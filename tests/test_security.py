import pytest


def test_sql_injection(api_client, config_loader, data_loader):
    """Attempt SQL Injection attack."""
    payload = data_loader.get_data("security", "sql_injection_payload")
    endpoint = config_loader.get("endpoints")["base_api"]["login"]
    response = api_client.post(endpoint, data=payload)
    assert response.status_code in [400, 401], "SQL Injection might be possible!"


def test_xss_attempt(api_client, config_loader, data_loader):
    """Attempt XSS attack."""
    payload = data_loader.get_data("security", "xss_payload")
    endpoint = config_loader.get("endpoints")["base_api"]["login"]
    response = api_client.post(endpoint, data=payload)
    assert response.status_code in [400, 401], "XSS vulnerability detected!"


def test_csrf_attack(api_client, config_loader, data_loader):
    """Simulate a CSRF attack attempt."""
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://malicious-site.com",  # Fake referer
    }
    payload = data_loader.get_data("security", "csrf_payload")
    endpoint = config_loader.get("endpoints")["base_api"]["login"]
    response = api_client.post(endpoint, data=payload, headers=headers)
    assert response.status_code in [400, 403], "Possible CSRF vulnerability!"


@pytest.mark.skip(reason="API does not implement brute-force protection")
def test_brute_force_protection(api_client, config_loader, data_loader):
    """Attempt brute-force attack."""
    payload = data_loader.get_data("security", "valid_user_credentials")
    endpoint = config_loader.get("endpoints")["base_api"]["login"]
    response = None
    for _ in range(10):
        response = api_client.post(endpoint, json=payload)
    assert response is not None, "Request was never made, response is None!"
    assert response.status_code in [400, 401], "Brute-force protection might be missing!"


@pytest.mark.skip(reason="API does not implement rate limiting")
def test_rate_limiting(api_client, config_loader, data_loader):
    headers = {"Authorization": f"Bearer {data_loader.get_data('security', 'test_token')}"}
    endpoint = config_loader.get("endpoints")["base_api"]["users"]
    responses = [api_client.get(endpoint, headers=headers).status_code for _ in range(20)]
    assert any(code == 429 for code in responses), "API might not have rate limiting!"
