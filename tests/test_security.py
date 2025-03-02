import pytest
import requests

BASE_URL = "https://reqres.in/api"


def test_sql_injection():
    """Attempt SQL Injection attack."""
    payload = {"email": "admin' OR 1=1 --", "password": "password"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code in [400, 401], "SQL Injection might be possible!"


def test_xss_attempt():
    """Attempt XSS attack."""
    payload = {"email": "<script>alert('xss')</script>", "password": "password"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code in [400, 401], "XSS vulnerability detected!"


def test_csrf_attack():
    """Simulate a CSRF attack attempt."""
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://malicious-site.com",  # Fake referer
    }
    payload = {"email": "victim@example.com", "password": "password123"}
    response = requests.post(f"{BASE_URL}/login", json=payload, headers=headers)

    assert response.status_code in [400, 403], "Possible CSRF vulnerability!"


def test_ssrf_attack():
    """Attempt an SSRF attack by requesting internal services."""
    payload = {"url": "http://localhost:8080/admin"}
    response = requests.post(f"{BASE_URL}/fetch-data", json=payload)

    assert response.status_code not in [200], "SSRF vulnerability detected!"


@pytest.mark.skip(reason="API does not implement brute-force protection")
def test_brute_force_protection():
    """Attempt brute-force attack."""
    payload = {"email": "eve.holt@reqres.in", "password": "wrongpassword"}

    response = None  # Initialize response to avoid 'referenced before assignment' error

    for _ in range(10):  # Simulating multiple login attempts
        response = requests.post(f"{BASE_URL}/login", json=payload)

    assert response is not None, "Request was never made, response is None!"
    assert response.status_code in [400, 401], "Brute-force protection might be missing!"


@pytest.mark.skip(reason="API does not implement rate limiting")
def test_rate_limiting():
    headers = {"Authorization": "Bearer test_token"}
    responses = [requests.get(f"{BASE_URL}/users", headers=headers).status_code for _ in range(20)]
    assert any(code == 429 for code in responses), "API might not have rate limiting!"

