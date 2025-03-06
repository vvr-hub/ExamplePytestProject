# Pytest API Test Automation Sample Project

## 📌 Overview

- This project is a Pytest-based API test automation framework that utilises a test API https://reqres.in/api
- It also utilises WireMock for mocking APIs.
- It supports functional testing, mock testing, fuzz testing, security testing, contract testing, negative testing, etc.
- The project provides some sample tests. The aim here is not to provide comprehensive test coverage.
- IMPORTANT NOTE: This is a **work in progress** project with scope for improvement.

## ⚡ Features

- **Pytest** for running API tests
- **WireMock** to mock API responses for endpoints which aren't yet developed/available for consumption
- **Docker** for seamless WireMock setup
- **Reporting** for test results and metrics using Allure
- **Centralised Configuration** for URLs and endpoints via `config.yaml`
- **Environment Configurability** Easily switch between different environments while running tests
- **Test data separation** from tests. Data is loaded dynamically from relevant file as per the target test environment
- **Parallelisation** for running tests simultaneously
- **Retries** for failing tests
- **Modular Structure** for easy test maintenance and scalability
- **Reusable** utils and fixtures, avoiding duplication of code
- **Reliable,** robust and independent tests, avoiding flakiness and hardcoding


---

### 🔧Recommended IDE

For optimal coding experience with this project, I recommend using **PyCharm Community Edition**.

---

## 🔧 Prerequisites

Ensure you have the following installed before setting up the project:

1. **Python 3.9+**
2. **Pipenv** (for dependency management):
   ```sh
   pip install pipenv
   ```
3. **Docker** (for WireMock container):

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
pytest -n 4 --reruns 3 -v --alluredir=allure-results
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
TEST_ENV=qa pytest -n 4 --reruns 3 -v --alluredir=allure-results
```

or simply as below (without setting the TEST_ENV)

```sh
pytest -n 4 --reruns 3 -v --alluredir=allure-results
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
different test environments, these imaginary environments are used. If we point to these environments, all tests
fail, except for the mocked endpoints.

### 6️⃣ View Test Reports for results and metrics using Allure

- Run Your Pytest Tests with Allure:
- Execute the Pytest tests with the --alluredir option. This option specifies the directory where Allure will store the test results.

```sh
pytest --alluredir=allure-results
```

- or with more specific requirements using the commands like below.

```sh
TEST_ENV=qa pytest -n auto --reruns 1 -v --alluredir=allure-results
```

- After the tests have finished, use the allure command-line tool to generate the HTML report from the results

```sh
allure serve allure-results
```

- Once the report finishes generating, the Allure Report will open in the browser.

---

## 📁 Project Structure

```
Note that the tests/ folder contains all test files.

📦 repo
├── 📂 tests
│   ├── conftest.py             # Setup, config and fixture management for the tests
│   ├── test_authentication.py  # Authentication tests
│   ├── test_contract.py        # Contract tests
│   ├── test_fuzz.py            # Basic Fuzz tests
│   ├── test_mock.py            # Mock tests
│   ├── test_negative.py        # Negative scenarios
│   ├── test_positive.py        # Happy path tests
│   ├── test_security.py        # Basic Security tests
│
├── 📂 utils                # Reusable functions
├── 📂 mocks                # Stubs
├── 📂 config               # Base URLs, endpoints and config loader
├── 📂 schemas              # JSON schemas for API contract testing
├── 📂 data                 # Test data files for each test environment and data loader
│   ├── qa.yaml                 # Data for Default Environment (QA Env)
│   ├── staging.yaml            # Data for Staging Environment
│   ├── demo.yaml               # Data for Demo Environment
│   ├── data_loader.py          # Data Loader
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
- **GitHub:** [vvr_hub]([https://github.com/vvr-hub]

---

## 🙏 Thanks And Acknowledgement

Many thanks to the provider(s) of the test API https://reqres.in/api
Thanks a lot, Ben Howdle. https://benhowdle.im/

---

### 🎯 Happy Testing! 🚀

