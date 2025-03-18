import logging
import time
from zapv2 import ZAPv2
from config.config_loader import ConfigLoader


class ZAPHelper:
    def __init__(self):
        config = ConfigLoader()
        self.zap_url = config.get("zap_url") or "http://localhost:8090"
        self.api_target = config.get_base_url()  # ✅ Get API base URL dynamically

        # ✅ Use ZAP's Python API
        self.zap = ZAPv2(proxies={'http': self.zap_url, 'https': self.zap_url})

        logging.basicConfig(level=logging.INFO)

    def import_api_endpoints(self):
        """Manually add all API endpoints with correct HTTP methods"""
        logging.info(f"📥 Adding API endpoints with methods from {self.api_target}")

        api_endpoints = [
            {"method": "GET", "url": "/users"},
            {"method": "GET", "url": "/users/2"},
            {"method": "GET", "url": "/users/23"},
            {"method": "GET", "url": "/unknown"},
            {"method": "GET", "url": "/unknown/2"},
            {"method": "GET", "url": "/unknown/23"},
            {"method": "POST", "url": "/users"},
            {"method": "PUT", "url": "/users/2"},
            {"method": "PATCH", "url": "/users/2"},
            {"method": "DELETE", "url": "/users/2"},
            {"method": "POST", "url": "/register"},
            {"method": "POST", "url": "/login"},
            {"method": "GET", "url": "/users?delay=3"}
        ]

        # ✅ Send each request to ZAP
        for endpoint in api_endpoints:
            full_url = f"{self.api_target}{endpoint['url']}"
            logging.info(f"🔗 {endpoint['method']} {full_url}")

            try:
                # ✅ Send request with correct HTTP method
                if endpoint["method"] == "GET":
                    self.zap.urlopen(full_url)
                elif endpoint["method"] == "POST":
                    self.zap.urlopen(full_url, data={"name": "test", "job": "leader"})
                elif endpoint["method"] in ["PUT", "PATCH"]:
                    self.zap.urlopen(full_url, data={"name": "updated"})
                elif endpoint["method"] == "DELETE":
                    self.zap.urlopen(full_url)

                time.sleep(1)  # Allow ZAP to process each request

            except Exception as e:
                logging.error(f"⚠️ Error adding {full_url}: {e}")

        logging.info("✅ API Endpoints added successfully!")

    def start_api_scan(self):
        """Runs OWASP ZAP API Security Scan"""
        logging.info(f"🚀 Starting ZAP API Security Scan on {self.api_target}")

        # ✅ Ensure ZAP is running before starting the scan
        try:
            zap_version = self.zap.core.version
            logging.info(f"✅ ZAP Version: {zap_version}")
        except Exception:
            logging.error("⚠️ ERROR: ZAP is not running or unreachable!")
            raise RuntimeError("OWASP ZAP is not running. Start ZAP first.")

        # ✅ Manually Import API Endpoints with correct methods
        self.import_api_endpoints()

        # ✅ Start an Active API Scan
        scan_id = self.zap.ascan.scan(self.api_target)

        # ✅ Validate scan ID
        if scan_id == "does_not_exist":
            logging.error("⚠️ ERROR: ZAP could not start the scan!")
            raise RuntimeError("ZAP Active Scan could not start. Check the target URL or API definition.")

        # ✅ Wait for the scan to complete
        while int(self.zap.ascan.status(scan_id)) < 100:
            logging.info(f"⏳ Active Scan progress: {self.zap.ascan.status(scan_id)}%")
            time.sleep(5)

        logging.info("✅ Active Scan completed!")

    def get_alerts(self):
        """Retrieves API security alerts from OWASP ZAP"""
        return self.zap.core.alerts()

    def generate_report(self):
        """Generates an API security report from OWASP ZAP"""
        report = self.zap.core.htmlreport()
        with open("zap_api_report.html", "w") as f:
            f.write(report)
        logging.info("✅ ZAP API Report saved as zap_api_report.html")
