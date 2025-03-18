import pytest


def test_sql_injection(api_client, config_loader, data_loader):
    """Attempt SQL Injection attack."""
    endpoint = config_loader.get_api_endpoints("login")
    payload = data_loader.get_data("security", "sql_injection_payload")

    response = api_client.post(endpoint, data=payload)

    assert response.status_code in [400, 401]


def test_xss_attempt(api_client, config_loader, data_loader):
    """Attempt XSS attack."""
    endpoint = config_loader.get_api_endpoints("login")
    payload = data_loader.get_data("security", "xss_payload")

    response = api_client.post(endpoint, data=payload)

    assert response.status_code in [400, 401]


def test_csrf_attack(api_client, config_loader, data_loader):
    """Simulate a CSRF attack attempt."""
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://malicious-site.com",
    }
    endpoint = config_loader.get_api_endpoints("login")
    payload = data_loader.get_data("security", "csrf_payload")

    response = api_client.post(endpoint, data=payload, headers=headers)

    assert response.status_code in [400, 403]


@pytest.mark.skip(reason="API does not implement brute-force protection")
def test_brute_force_protection(api_client, config_loader, data_loader):
    """Attempt brute-force attack."""
    endpoint = config_loader.get_api_endpoints("login")
    payload = data_loader.get_data("security", "valid_user_credentials")

    response = None
    for _ in range(10):
        response = api_client.post(endpoint, json=payload)

    assert response is not None
    assert response.status_code in [400, 401]


@pytest.mark.skip(reason="API does not implement rate limiting")
def test_rate_limiting(api_client, config_loader, data_loader):
    """Test API rate limiting."""
    headers = {"Authorization": f"Bearer {data_loader.get_data('security', 'test_token')}"}
    endpoint = config_loader.get_api_endpoints("users")

    responses = [api_client.get(endpoint, headers=headers).status_code for _ in range(20)]

    assert any(code == 429 for code in responses)
