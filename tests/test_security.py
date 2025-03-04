import pytest


def test_sql_injection(api_client, config_loader):
    """Attempt SQL Injection attack."""
    payload = {"email": "admin' OR 1=1 --", "password": "password"}
    endpoint = config_loader.get("endpoints")["base_api"]["login"]
    response = api_client.post(endpoint, data=payload)
    assert response.status_code in [400, 401], "SQL Injection might be possible!"


def test_xss_attempt(api_client, config_loader):
    """Attempt XSS attack."""
    payload = {"email": "<script>alert('xss')</script>", "password": "password"}
    endpoint = config_loader.get("endpoints")["base_api"]["login"]
    response = api_client.post(endpoint, data=payload)
    assert response.status_code in [400, 401], "XSS vulnerability detected!"


def test_csrf_attack(api_client, config_loader):
    """Simulate a CSRF attack attempt."""
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://malicious-site.com",  # Fake referer
    }
    payload = {"email": "victim@example.com", "password": "password123"}
    endpoint = config_loader.get("endpoints")["base_api"]["login"]
    response = api_client.post(endpoint, data=payload, headers=headers)

    assert response.status_code in [400, 403], "Possible CSRF vulnerability!"


@pytest.mark.skip(reason="API does not implement brute-force protection")
def test_brute_force_protection(api_client, config_loader):
    """Attempt brute-force attack."""
    payload = {"email": "eve.holt@reqres.in", "password": "wrongpassword"}
    endpoint = config_loader.get("endpoints")["base_api"]["login"]

    response = None  # Initialise response to avoid 'referenced before assignment' error

    for _ in range(10):  # Simulating multiple login attempts
        response = api_client.post(endpoint, json=payload)

    assert response is not None, "Request was never made, response is None!"
    assert response.status_code in [400, 401], "Brute-force protection might be missing!"


@pytest.mark.skip(reason="API does not implement rate limiting")
def test_rate_limiting(api_client, config_loader):
    headers = {"Authorization": "Bearer test_token"}
    endpoint = config_loader.get("endpoints")["base_api"]["users"]
    responses = [api_client.get(endpoint, headers=headers).status_code for _ in range(20)]
    assert any(code == 429 for code in responses), "API might not have rate limiting!"
