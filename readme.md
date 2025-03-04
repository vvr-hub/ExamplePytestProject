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
- **Centralized Configuration** for URLs and endpoints via `config.yaml`
- **Environment Configurability** Easily switch between different environments while running tests
- **Parallelization** for running tests simultaneously
- **Retries** for failing tests
- **Reliability** Robust and independent tests free from flakiness

---

### 🔧Recommended IDE

For optimal coding experience with this project, I recommend using **PyCharm Community Edition**.

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

### 3️⃣ Rerunning Failing Tests

- Rerun all failing tests 2 times

```sh
pytest --reruns 2
```

- Rerun a specific test file 2 times

```sh
pytest tests/test_security.py --reruns 2
```

- Rerun a specific test function 2 times

```sh
pytest tests/test_security.py::test_sql_injection --reruns 2
```

- Rerun tests matching a keyword 2 times

```sh
pytest -k "security" --reruns 2
```

- Add a 1-second delay between retries

```sh
pytest --reruns 2 --reruns-delay 1
```

### 4️⃣ Running Tests in Parallel

- Run tests using all available CPU cores:

```sh
pytest -n auto
```

- Run tests using a specific number of worker processes, for example 4

```sh
pytest -n 4
```

- Run tests in parallel with verbose output

```sh
pytest -n auto -v
```

- Load Balancing (loadscope)

```sh
pytest -n 4 --dist=loadscope
```

- Run Tests in Parallel and Retrying Failing Tests (example with 3 retries)

```sh
pytest -n 4 --reruns 3 -v
```

- Run Tests in Parallel, with retries (for Failing Tests), and HTML Report generated

```sh
pytest -n 4 --reruns 3 -v --html=report.html
```

### 5️⃣ Setting the desired environment to run tests

- To run tests on the default environment (QA env).

If no TEST_ENV is set, it defaults to QA.

```sh
pytest -n auto
```

- You can explicitly set the environment to QA

```sh
TEST_ENV=qa pytest -n auto
```

- To run tests on QA environment in parallel with retries and report generation

```sh
TEST_ENV=qa pytest -n 4 --reruns 3 -v --html=report.html
```

or simply as below (without setting the TEST_ENV)

```sh
pytest -n 4 --reruns 3 -v --html=report.html
```

- To run tests against Staging environment

```sh
TEST_ENV=staging pytest
```

- To run tests against Demo environment

```sh
TEST_ENV=demo pytest
```

**NOTE:** The demo and staging environments do not exist. To demonstrate the project's capability to switch between
different test environments, these imaginary environments are specified. If we point to these environments, all tests
fail, except for the mocked endpoints.

### 6️⃣ Generate HTML Test Report

```sh
pytest --html=report.html
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
├── 📂 schemas              # JSON schemas for API contract testing
│
├── conftest.py             # Useful in the future for global test fixtures, etc
├── pytest.ini              # Pytest configurations
├── report.html             # Test Report showing results
├── requirements.txt        # Dependencies
├── README.md               # Project documentation

```

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

