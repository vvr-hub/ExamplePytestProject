import logging
import time
from zapv2 import ZAPv2
from config.config_loader import ConfigLoader


class ZAPHelper:
    def __init__(self):
        config = ConfigLoader()
        self.zap_url = config.get("zap_url") or "http://localhost:8090"
        self.api_target = config.get_base_url()  # Get API base URL dynamically

        # ✅ Use ZAP's Python API
        self.zap = ZAPv2(proxies={'http': self.zap_url, 'https': self.zap_url})

        logging.basicConfig(level=logging.INFO)

    def import_api_endpoints(self):
        """Manually add all API endpoints for scanning"""
        logging.info(f"📥 Manually adding API endpoints from {self.api_target}")

        api_endpoints = [
            "/users", "/users/2", "/users/23",  # Users (list, single, not found)
            "/unknown", "/unknown/2", "/unknown/23",  # Resources (list, single, not found)
            "/users", "/users/2", "/users/2", "/users/2",  # Create, Update, Update, Delete
            "/register", "/register",  # Register (success & failure)
            "/login", "/login",  # Login (success & failure)
            "/users?delay=3"  # Delayed response
        ]

        # ✅ Add each endpoint manually to ZAP Spider
        for endpoint in api_endpoints:
            full_url = f"{self.api_target}{endpoint}"
            logging.info(f"🔗 Adding {full_url} to ZAP Spider")
            self.zap.urlopen(full_url)
            time.sleep(1)  # Allow ZAP to process each request

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

        # ✅ Manually Import API Endpoints
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
