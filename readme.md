# Pytest API & Websockets Test Automation Project (Sample)

![CI](https://github.com/vvr-hub/ExamplePytestProject/actions/workflows/tests-in-ci.yml/badge.svg)

## 📌 Overview

- This project is a Pytest-based API test automation framework that utilises a test API https://reqres.in/api
- It also utilises WireMock for mocking APIs.
- Supports functional testing, mock testing, fuzz testing, security testing, contract testing, negative testing, etc.
- **Security tests** using **OWASP ZAP** help detect **API vulnerabilities** such as **CORS misconfigurations,
  authentication flaws, injection attacks, sensitive data exposure, and more.**
- The project provides some sample tests. The aim here is not to provide comprehensive test coverage.
- There are also some tests for **websockets**
- IMPORTANT NOTE: This is a **work in progress** project with scope for improvement.

## ⚡ Features

- **Pytest** for running API tests
- **OWASP ZAP Security Scanning** for detecting API security vulnerabilities.
- **WireMock** to mock API responses for endpoints which aren't yet developed/available for consumption
- **Docker** for seamless WireMock setup
- **Reporting** for test results and metrics using Allure
- **Centralised Configuration** for URLs and endpoints via `config.yaml`
- **Environment Configurability** Easily switch between different environments while running tests
- **Test data separation** from tests. Data is loaded dynamically from relevant file as per the target test environment
- **Parallelisation** for running tests simultaneously
- **Retries** for failing tests
- ✅ GitHub Actions **CI Pipeline** to run the tests
- **Modular Structure** for easy test maintenance and scalability
- **Reusable** utils and fixtures, avoiding duplication of code
- **Reliable,** robust and independent tests, avoiding flakiness and hardcoding

---

## Disclaimer:

The **security testing tools and scripts** provided in this project are intended solely for educational purposes and to
facilitate security testing on APIs you own or have explicit permission to test. Do not use these tools to conduct
security tests on the **https://reqres.in/ API or any other third-party APIs** without proper authorisation. *
*Unauthorised security testing** may violate legal agreements and could lead to legal action. By using these tools, you
agree to take **full responsibility** for ensuring that your use complies with all applicable **laws and regulations**.


---

### 🔧Recommended IDE

For optimal coding experience with this project, I recommend using **PyCharm Community Edition**.

---

## 🔧 Prerequisites

Ensure you have the following installed before setting up the project:

1. **Git**

- Download: [Git Downloads](https://git-scm.com/downloads)
- Installation Guide: [Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

2. **Python 3.9+**

- Download: [Python Downloads](https://www.python.org/downloads/)
- Installation Guide: [Installing Python](https://docs.python.org/3/using/index.html)

3. **Pipenv**

- Installation Guide: [Pipenv Installation](https://pipenv.pypa.io/en/latest/install/)
- Run the following command after installing Python:
   ```sh
   pip install pipenv
   ```

4. **Docker** (for WireMock container):

- [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)


5. **OWASP ZAP** (for the security testing of the API)

- OWASP ZAP can be downloaded from the official website:
  [OWASP ZAP Download](https://www.zaproxy.org/download/)

To verify installation:

```sh
git --version
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
   source . venv/bin/activate
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Ensure Docker is Running**

   If Docker is not running, start it manually. Refer to the below section on Docker if required.

---

## 🐳 Docker Desktop and WireMock Setup

After you download Docker, follow the below instructions.

---

1. **Install Docker Desktop**

To run WireMock in a Docker container, you need to have Docker Desktop installed on your machine.

- **macOS**:
    - Download Docker Desktop for macOS from [here](https://www.docker.com/products/docker-desktop).
    - Follow the instructions to install Docker Desktop.

- **Windows**:
    - Download Docker Desktop for Windows from [here](https://www.docker.com/products/docker-desktop).
    - Follow the installation instructions for Windows.

- **Linux**:
    - Follow the installation guide for Docker on [Linux](https://docs.docker.com/engine/install/) for your specific
      distribution.

Once the installation is complete, Docker Desktop should be available from your applications menu or start menu.

2. **Verify Docker Installation**

After installing Docker Desktop, verify that Docker is properly installed and running.

Open a terminal or command prompt and run the following command:

```sh
docker --version
```

This should return the installed Docker version. To confirm Docker is running, you can use:

```sh
docker info
```

If Docker is running correctly, this will display information about your Docker installation.

3. **Install and Run WireMock in a Docker Container**
   To run WireMock in a Docker container, you can use the official WireMock image from Docker Hub.

Run the following command to pull the WireMock Docker image:

```sh
docker pull wiremock/wiremock
```

Next, start the WireMock container by running:

```sh
docker run -d --name wiremock -p 8080:8080 wiremock/wiremock
```

This will:

- Download the WireMock Docker image (if not already pulled).
- Run the container in detached mode (`-d`).
- Map port `8080` on your machine to port `8080` in the container, so WireMock can be accessed from
  `http://localhost:8080`

4. **Managing the WireMock Container**

To **list all running Docker containers**, use:

```sh
docker ps
```

This will show you the running WireMock container along with its status and other details.

If you need to **start the WireMock container** after stopping it, run:

```sh
docker start wiremock
```

This will start the WireMock container again.

To **stop the WireMock** container, run:

```sh
docker stop wiremock

```

This will stop the container, but it can be started again using the **docker start** command as shown above.


---

## 🛠 OWASP ZAP Integration Setup

OWASP ZAP is used for automated API security testing.

### 1️⃣ Install OWASP ZAP

1. Download **OWASP ZAP** from the official website.
2. Open the downloaded `.dmg` file and move `ZAP.app` to the `/Applications` folder.
3. Eject the mounted volume.

### 2️⃣ Add ZAP to System PATH

To enable running `zap.sh` from anywhere:

```sh
nano ~/.zshrc
```

Add the following line at the bottom:

```sh
export PATH="$PATH:/Applications/ZAP.app/Contents/Java"
```

Save (`CTRL + X', then `Y`, then `Enter`).  
Apply changes:

```sh
source ~/.zshrc
```

Verify installation:

```sh
which zap.sh
```

Expected output:

```swift
/Applications/ZAP.app/Contents/Java/zap.sh
```

### 3️⃣ Start OWASP ZAP in Daemon Mode

Run ZAP in the `background mode` (headless):

```sh
zap.sh -daemon -port 8090
```

This makes ZAP listen on `port 8090` for API security testing.
Verify ZAP is running:

```sh
curl http://localhost:8090/JSON/core/view/version/
```

Expected response:

```json
{
  "version": "2.16.0"
}
```

Check if ZAP is listening on port `8090`:

```sh
lsof -i :8090
```

Expected output:

```pgsql
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java    36987   vr  242u  IPv6 0xc983ecdaee0df363      0t0  TCP localhost:8090 (LISTEN)
```

### 4️⃣ Disable API Key Protection (GUI)

1. Open OWASP ZAP GUI:

```sh
open /Applications/ZAP.app
```

🔸 Disable API Key:

1. Go to `Tools → Options → API`.
2. Tick the checkbox for `"Disable API Key"`.
3. Restart ZAP.

### 5️⃣ Run Only the Security Test (Using OWASP ZAP)

Make sure ZAP is running (in daemon mode). Then run the following command

```sh
 pytest tests/test_security_scan_api.py
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

### 3️⃣ Run a Specific function inside a test

```sh
pytest -k "test_specific_function"
```

### 4️⃣ Rerunning Failing Tests

- Rerun all failing tests 2 times

```sh
pytest --reruns 2
```

- Rerun a specific test file 2 times

```sh
pytest tests/test_positive.py --reruns 2
```

- Rerun a specific test function 2 times

```sh
pytest tests/test_positive.py::test_get_users_pages --reruns 2
```

- Rerun tests matching a keyword 2 times

```sh
pytest -k "fuzz" --reruns 2
```

- Add a 1-second delay between retries

```sh
pytest --reruns 2 --reruns-delay 1
```

### 5️⃣ Running Tests in Parallel

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

### 6️⃣ Setting the desired environment to run tests

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

or simply as below (without setting the `TEST_ENV`)

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
different test environments, these imaginary environments are used. If we point to these environments, all API tests
fail, except for the mocked endpoints. (The websockets tests still pass.)

### 7️⃣ View Test Reports for results and metrics using Allure

- Run Your Pytest Tests with Allure:
- Execute the Pytest tests with the --alluredir option. This option specifies the directory where Allure will store the
  test results.

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

### 8️⃣ View ZAP Security Report

After the OWASP ZAP aided security test completes (either alone or as part of the full suite), open the report:

```sh
open zap_api_report.html
```

The `SamplePytestProject/docs/` folder has got screenshots of a sample OWASP ZAP Report.

---

## ✅ CI/CD with GitHub Actions

This project includes a GitHub Actions workflow to automatically run all tests using Pytest, WireMock and Allure.

### 🧪 What the Workflow Does

- Automatically starts **WireMock** inside a Docker container
- Installs dependencies from `requirements.txt`
- Runs tests using:

```sh
  TEST_ENV=qa pytest -n auto --reruns 1 -v --alluredir=allure-results
 ```

- Generates an Allure Report from test results
- Uploads the report as an artifact

### 📁 How to View the Allure Report

1. Go to the Actions tab
2. Click the latest workflow run
3. Download the allure-report artifact
4. Extract it locally
5. Open index.html in your browser

#### 💡 NOTE:
If you double-click `index.html`, the report may show only "Loading...".  
To properly view the Allure report, serve it with a local web server.  
1. Switch to the folder (`allure-report/`) where `index.html` is downloaded on your machine.  
2. Run the below.  
```sh
python3 -m http.server 8000
```
3. Then open: http://localhost:8000

### 📄 Workflow File

.github/workflows/tests-in-ci.yml

---

## 📁 Project Structure

```

Note that the tests/ folder contains all test files.

📦 repo
├── 📂 tests
│ ├── conftest.py               # Setup, config & fixture management for the tests
│ ├── test_authentication.py    # Authentication tests
│ ├── test_contract.py          # Contract tests
│ ├── test_fuzz.py              # Basic Fuzz tests
│ ├── test_mock.py              # Mock tests
│ ├── test_negative.py          # Negative scenarios
│ ├── test_positive.py          # Happy path tests
│ ├── test_security.py          # Basic Security tests
│ ├── test_security_scan_api.py # OWASP ZAP aided Security Test
│ ├── 📂 websockes            
│ ├── conftest.py               # Setup
│ ├── test_websocket.py         # Basic Websockets tests      
│
├── 📂 utils               # Reusable functions (including OWASP ZAP helper)
├── 📂 mocks               # Stubs
├── 📂 config              # Base URLs, endpoints and config loader
├── 📂 schemas             # JSON schemas for API contract testing
├── 📂 data                # Test data files for each test environment and data loader
│ ├── qa.yaml              # Data for Default Environment (QA Env)
│ ├── staging.yaml         # Data for Staging Environment
│ ├── demo.yaml            # Data for Demo Environment
│ ├── data_loader.py       # Data Loader
│
├── conftest.py            # For global test fixtures (Ex: initialising ZAP for security scanning)
├── pytest.ini             # Pytest configurations
├── report.html            # Test Report showing results
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
├── 📂 docs/               # Screenshots of some parts of OWASP ZAP Security Test Report.
├── 📂 .github/workflows/  # Contains GitHub Actions workflow file for running tests & generating Allure reports
automatically.

```

---

## 🔒 Integrating OWASP ZAP with the pytest project

This approach enhances security by **automating vulnerability detection** during API testing, ensuring **early issue
identification**. It seamlessly integrates with the existing tests using pytest fixtures, enabling **continuous security
assessments** in a DevSecOps workflow. **ZAP's detailed reports** provide insights into security risks, aiding quick
remediation. While it adds some setup complexity, the **long-term benefits** (proactive security, automation and
improved test coverage) outweigh the effort, making the **API more resilient** against threats. 🚀

---

## 🙏 Thanks And Acknowledgement

Many thanks to the provider(s) of the test API https://reqres.in/api
Thanks a lot, Ben Howdle. https://benhowdle.im/
Many thanks also to the providers of Postman Echo WebSocket wss://ws.postman-echo.com/raw

---

### 🎯 Happy Testing! 🚀
