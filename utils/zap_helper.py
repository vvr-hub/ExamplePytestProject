import logging
import time
from zapv2 import ZAPv2
from config.config_loader import ConfigLoader


class ZAPHelper:
    def __init__(self):
        config = ConfigLoader()  # ✅ Load config only once inside the class
        zap_url = config.get("zap_url") or "http://localhost:8090"
        self.zap = ZAPv2(proxies={'http': zap_url, 'https': zap_url})
        logging.basicConfig(level=logging.INFO)

    def start_spider(self, target):
        logging.info(f"Starting ZAP Spider for {target}")
        try:
            scan_id = self.zap.spider.scan(target)
            logging.info(f"ZAP Spider scan started: {scan_id}")

            while int(self.zap.spider.status(scan_id)) < 100:
                logging.info(f"Spider progress: {self.zap.spider.status(scan_id)}%")
                time.sleep(2)
            logging.info("Spider scan completed")
        except Exception as e:
            logging.error(f"Error starting ZAP Spider: {e}")
            raise

    def start_active_scan(self, target):
        logging.info(f"Starting Active Scan for {target}")
        try:
            scan_id = self.zap.ascan.scan(target)
            logging.info(f"ZAP Active scan started: {scan_id}")

            while int(self.zap.ascan.status(scan_id)) < 100:
                logging.info(f"Active Scan progress: {self.zap.ascan.status(scan_id)}%")
                time.sleep(5)
            logging.info("Active Scan completed")
        except Exception as e:
            logging.error(f"Error starting ZAP Active Scan: {e}")
            raise

    def generate_report(self, filename="zap_report.html"):
        """Generates an HTML security report from ZAP scans."""
        report = self.zap.core.htmlreport()
        with open(filename, "w") as f:
            f.write(report)
        logging.info(f"ZAP report saved as {filename}")

    def get_alerts(self):
        """Fetches security alerts from ZAP after the scan."""
        return self.zap.core.alerts()
