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

        # Fix: Ensure api_endpoints is a list of dicts
        self.api_endpoints = config.get("api_endpoints", [])

        self.zap = ZAPv2(proxies={'http': self.zap_url, 'https': self.zap_url})
        logging.basicConfig(level=logging.INFO)

    def send_requests_to_zap(self):
        """Send API requests dynamically from config.yaml"""
        logging.info("📥 Sending API requests to ZAP for traffic analysis")
        headers = {"Content-Type": "application/json"}

        for endpoint in self.api_endpoints:
            full_url = f"{self.api_target}{endpoint['url']}"
            method = endpoint.get("method", "GET").upper()
            data = endpoint.get("data", {})

            logging.info(f"🔗 {method} {full_url}")

            try:
                response = requests.request(
                    method,
                    full_url,
                    json=data if data else None,
                    headers=headers,
                    proxies={'http': self.zap_url, 'https': self.zap_url},
                    verify=False  # ✅ Bypass SSL verification
                )
                response.raise_for_status()
                time.sleep(1)  # Allow ZAP to process each request
            except Exception as e:
                logging.error(f"⚠️ Error sending {method} {full_url}: {e}")

        logging.info("✅ API Requests sent successfully!")

    def start_api_scan(self):
        """Runs OWASP ZAP API Security Scan"""
        logging.info(f"🚀 Starting ZAP API Security Scan on {self.api_target}")

        # ✅ Ensure ZAP is running before scanning
        try:
            zap_version = self.zap.core.version
            logging.info(f"✅ ZAP Version: {zap_version}")
        except Exception:
            logging.error("⚠️ ERROR: ZAP is not running or unreachable!")
            raise RuntimeError("OWASP ZAP is not running. Start ZAP first.")

        # ✅ Send API requests first to populate ZAP with traffic
        self.send_requests_to_zap()

        # ✅ Start an Active API Scan
        scan_id = self.zap.ascan.scan(self.api_target)
        if scan_id == "does_not_exist":
            logging.error("⚠️ ERROR: ZAP could not start the scan!")
            raise RuntimeError("ZAP Active Scan could not start. Check the target URL or API definition.")

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
