# Pytest API Test Automation Sample Project

## 📌 Overview

- This project is a Pytest-based API test automation framework that utilises a test API https://reqres.in/api
- It also utilises WireMock for mocking APIs.
- It supports functional testing, mock testing, fuzz testing, security testing, contract testing, negative testing, etc.
- The project provides some sample tests. The aim here is not to provide comprehensive test coverage.
- IMPORTANT NOTE: This is a **work in progress** project with scope for improvement and adopting best practices.

## ⚡ Features

- **Pytest** for running API tests
- **WireMock** for mocking API responses
- **Docker** for seamless WireMock setup
- **Logging & Reporting** for detailed test insights
- **Modular Structure** for easy test maintenance
- **Centralized Configuration** for URLs via `config.yaml`

---

## 🔧 Prerequisites

Ensure you have the following installed before setting up the project:

1. **Python 3.9+** [Download here](https://www.python.org/downloads/)
2. **Pipenv** (for dependency management):
   ```sh
   pip install pipenv
   ```
3. **Docker** (for WireMock container):
    - [Mac & Windows](https://www.docker.com/products/docker-desktop/)
    - [Linux](https://docs.docker.com/engine/install/)

To verify installation:

```sh
python --version
pipenv --version
docker --version
```

---

## 🚀 Setup & Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/vvr-hub/ExamplePytestProject.git
   cd SamplePytestProject
   ```
2. **Create and Activate Virtual Environment**
   ```sh
   pipenv install
   pipenv shell
   
   python3 -m venv venv
   . venv/bin/activate
   ```
3. **Ensure Docker is Running**

   If Docker is not running, start it manually.
   ```sh
   docker info
   ```

4. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

---

## 🛠 Running the Tests

### 1️⃣ Run All Tests

```sh
pytest
```

### 2️⃣ Run a Specific Test File

```sh
pytest tests/test_mock.py
```

### 2️⃣ Run a Specific function inside a test

```sh
pytest -k "test_specific_function"
```

### 3️⃣ Run Tests with Detailed Logs

```sh
pytest -v
```

### 4️⃣ Generate HTML Test Report

```sh
pytest --html=report.html
```

### 5️⃣ Stop WireMock (if needed)

```sh
docker stop wiremock
```

---

## 📁 Project Structure

```
Note that the tests/ folder contains all test files.

📦 repo
├── 📂 tests
│   ├── conftest.py                   # WireMock setup
│   ├── test_authentication.py        # Authentication tests
│   ├── test_contract.py              # Contract tests
│   ├── test_fuzz.py                  # Fuzz tests
│   ├── test_mock.py                  # Mock tests
│   ├── test_negative.py              # Negative tests
│   ├── test_positive.py              # Positive tests
│   ├── test_security.py              # Security tests
│
├── 📂 utils
├── 📂 mocks
├── 📂 config
│
├── conftest.py             # Useful in the future for global test fixtures, etc
├── pytest.ini              # Pytest configurations
├── report.html             # Test Report showing results
├── requirements.txt        # Dependencies
├── README.md               # Project documentation

```

---

## 🔄 WireMock Stub Configuration (Automatic)

WireMock is automatically configured using `conftest.py`. If you need to manually add stubs, use:

```sh
curl -X POST "http://localhost:8080/__admin/mappings" \
  -H "Content-Type: application/json" \
  -d '{
    "request": {"method": "GET", "url": "/mocked-user"},
    "response": {
      "status": 200,
      "body": "{\"id\": 1, \"name\": \"Mock User\"}",
      "headers": {"Content-Type": "application/json"}
    }
  }'
```

---

## 📌 Best Practices

- Keep test cases modular and independent.
- Use `pytest fixtures` for test setup & teardown.
- Always validate API response codes and payloads.
- Maintain clear documentation.

---

## 📝 Author

- **Venki Rao**
- **GitHub:** [vvr_hub](https://github.com/your-username)

---

## 🙏 Thanks And Acknowledgement


Many thanks to the provider(s) of the test API https://reqres.in/api
Thanks a lot, Ben Howdle. https://benhowdle.im/

---

### 🎯 Happy Testing! 🚀

