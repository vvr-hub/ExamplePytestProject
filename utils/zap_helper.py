import logging
import time
import requests
from zapv2 import ZAPv2
from config.config_loader import ConfigLoader


class ZAPHelper:
    def __init__(self):
        config = ConfigLoader()
        self.zap_url = config.get("zap_url") or "http://localhost:8090"
        self.api_target = config.get_base_url()

        # Use ZAP's Python API
        self.zap = ZAPv2(proxies={'http': self.zap_url, 'https': self.zap_url})

        logging.basicConfig(level=logging.INFO)

    def send_requests_to_zap(self):
        """Send API requests with correct HTTP methods to ZAP before scanning."""
        logging.info(f"📥 Sending API requests to ZAP for traffic analysis")

        api_endpoints = [
            {"method": "GET", "url": "/users"},
            {"method": "GET", "url": "/users/2"},
            {"method": "POST", "url": "/users", "data": {"name": "test", "job": "leader"}},
            {"method": "PUT", "url": "/users/2", "data": {"name": "updated"}},
            {"method": "PATCH", "url": "/users/2", "data": {"name": "patched"}},
            {"method": "DELETE", "url": "/users/2"},
            {"method": "POST", "url": "/register", "data": {"email": "eve.holt@reqres.in", "password": "pistol"}},
            {"method": "POST", "url": "/login", "data": {"email": "eve.holt@reqres.in", "password": "cityslicka"}},
            {"method": "GET", "url": "/users?delay=3"}
        ]

        headers = {"Content-Type": "application/json"}

        for endpoint in api_endpoints:
            full_url = f"{self.api_target}{endpoint['url']}"
            method = endpoint["method"]
            data = endpoint.get("data", {})

            logging.info(f"🔗 {method} {full_url}")

            try:
                # Bypass SSL verification using `verify=False`
                if method == "GET":
                    requests.get(full_url, headers=headers, proxies={'http': self.zap_url, 'https': self.zap_url},
                                 verify=False)
                elif method == "POST":
                    requests.post(full_url, json=data, headers=headers,
                                  proxies={'http': self.zap_url, 'https': self.zap_url}, verify=False)
                elif method == "PUT":
                    requests.put(full_url, json=data, headers=headers,
                                 proxies={'http': self.zap_url, 'https': self.zap_url}, verify=False)
                elif method == "PATCH":
                    requests.patch(full_url, json=data, headers=headers,
                                   proxies={'http': self.zap_url, 'https': self.zap_url}, verify=False)
                elif method == "DELETE":
                    requests.delete(full_url, headers=headers, proxies={'http': self.zap_url, 'https': self.zap_url},
                                    verify=False)

                time.sleep(1)  # Allow ZAP to process each request

            except Exception as e:
                logging.error(f"⚠️ Error sending {method} {full_url}: {e}")

        logging.info("✅ API Requests sent successfully!")

    def start_api_scan(self):
        """Runs OWASP ZAP API Security Scan"""
        logging.info(f"🚀 Starting ZAP API Security Scan on {self.api_target}")

        # Ensure ZAP is running before scanning
        try:
            zap_version = self.zap.core.version
            logging.info(f"✅ ZAP Version: {zap_version}")
        except Exception:
            logging.error("⚠️ ERROR: ZAP is not running or unreachable!")
            raise RuntimeError("OWASP ZAP is not running. Start ZAP first.")

        # Send API requests first to populate ZAP with traffic
        self.send_requests_to_zap()

        # Start an Active API Scan
        scan_id = self.zap.ascan.scan(self.api_target)

        # Validate scan ID
        if scan_id == "does_not_exist":
            logging.error("⚠️ ERROR: ZAP could not start the scan!")
            raise RuntimeError("ZAP Active Scan could not start. Check the target URL or API definition.")

        # Wait for the scan to complete
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
