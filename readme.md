# Pytest API Test Automation Framework

## 📌 Overview
This project is a Pytest-based API test automation framework that utilizes WireMock for mocking APIs. It supports integration, unit, and mock testing, ensuring comprehensive test coverage.

## ⚡ Features
- **Pytest** for running API tests
- **WireMock** for mocking API responses
- **Docker** for seamless WireMock setup
- **Logging & Reporting** for detailed test insights
- **Modular Structure** for easy test maintenance

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
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. **Create and Activate Virtual Environment**
   ```sh
   pipenv install
   pipenv shell
   ```
3. **Ensure Docker is Running**
   ```sh
   docker info
   ```
   If Docker is not running, start it manually.


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
📦 your-repo
├── 📂 tests
│   ├── test_unit.py        # Unit tests
│   ├── test_integration.py # Integration tests
│   ├── test_mock.py        # Mock API tests
│
├── conftest.py             # Global test fixtures & WireMock setup
├── Pipfile                 # Pipenv dependencies
├── Pipfile.lock            # Dependency lock file
├── README.md               # Project documentation
├── pytest.ini              # Pytest configurations
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
- **Your Name**  
- **GitHub:** [your-username](https://github.com/your-username)

---
### 🎯 Happy Testing! 🚀

