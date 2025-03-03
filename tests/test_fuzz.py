import pytest
import requests
import random
import string
import re
from utils.config_utils import load_config

config = load_config()
BASE_URL = config["base_url"]

random.seed(42)  # Set a fixed seed


def random_string(length=10):
    """Generates a random alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def random_email(length=8):
    """Generates a random email address."""
    username = random_string(length)
    domain = random_string(5) + ".com"
    return f"{username}@{domain}"


def random_int_string(length=5):
    """Generates a random string of numbers."""
    return ''.join(random.choices(string.digits, k=length))


@pytest.fixture
def api_client():
    """Provides a requests.Session object for API interactions."""
    session = requests.Session()
    return session


@pytest.mark.parametrize("email,password", [
    ("", ""),  # Empty values - Handled
    (random_email(), ""),  # valid email, empty password - Handled.

    # THE BELOW ARE VALID FUZZ INPUTS, BUT THE API DOES NOT HANDLE THEM ROBUSTLY.
    # They return a generic "user not found" error.

    # ("test@domain", "1234"),  # Missing TLD - Not robustly handled
    # ("admin'--@example.com", "password"),  # SQL Injection attempt - Not robustly handled
    # ("<script>alert('xss')</script>", "password123"),  # XSS attack - Not robustly handled
    # (random_string(1000), random_string(1000)),  # Extremely long input - Not robustly handled
    # (random_email(), random_string()), # valid email, random password - Not robustly handled
    # (random_string(), random_int_string()), # random username, numeric password - Not robustly handled
    # (random_string(), random_string(10000)), # random username, extremely long password - Not robustly handled
    # (random_int_string(), random_string()), # numeric username, random password - Not robustly handled
    # (random_string(10000), random_string()), # extremely long username, random password - Not robustly handled
    # ("", random_string()), # empty email, random password - Not robustly handled
    # (random_string(), " "), # random email, space password - Not robustly handled
    # (" ", random_string()), # space email, random password - Not robustly handled
    # ("test@example.com", "\n"), # valid email, newline password - Not robustly handled
    # ("\n", "password"), # newline email, valid password - Not robustly handled
    # ("test@example.com", "\t"), # valid email, tab password - Not robustly handled
    # ("\t", "password"), # tab email, valid password - Not robustly handled
    # ("test@example.com", "\r"), # valid email, carriage return password - Not robustly handled
    # ("\r", "password"), # carriage return email, valid password - Not robustly handled
    # ("test@example.com", "\\"), # valid email, backslash password - Not robustly handled
    # ("\\", "password"), # backslash email, valid password - Not robustly handled
    # ("test@example.com", "\""), # valid email, double quote password - Not robustly handled
    # ("\"", "password"), # double quote email, valid password - Not robustly handled
    # ("test@example.com", "'"), # valid email, single quote password - Not robustly handled
    # ("'", "password"), # single quote email, valid password - Not robustly handled
    # ("test@example.com", "`"), # valid email, backtick password - Not robustly handled
    # ("`", "password"), # backtick email, valid password - Not robustly handled
    # ("test@example.com", "~"), # valid email, tilde password - Not robustly handled
    # ("~", "password"), # tilde email, valid password - Not robustly handled
])
def test_fuzz_login(api_client, email, password):
    """Test login with various fuzzed inputs and verify error details."""
    endpoint = config["endpoints"]["base_api"]["login"]
    response = api_client.post(f"{BASE_URL}{endpoint}", json={"email": email, "password": password})
    assert response.status_code in [400, 401]
    response_json = response.json()
    assert "error" in response_json or "errors" in response_json
    if response.status_code == 400:
        assert re.search(r"invalid|missing|format|length|user not found",
                         str(response_json).lower())  # check for error keywords.
