import pytest
import logging
from config.config_loader import ConfigLoader

config = ConfigLoader()
base_url = config.get_base_url()


@pytest.mark.security
def test_security_scan(zap):
    """Runs an automated security scan using OWASP ZAP"""
    logging.info(f"Starting ZAP Security Scan on {base_url}")

    # Start Spider & Active Scan
    zap.start_spider(base_url)
    zap.start_active_scan(base_url)

    alerts = zap.get_alerts()  # Fetch alerts from ZAP

    # Categorising vulnerabilities
    high_risk = [alert for alert in alerts if alert["risk"] == "High"]
    medium_risk = [alert for alert in alerts if alert["risk"] == "Medium"]
    low_risk = [alert for alert in alerts if alert["risk"] == "Low"]
    informational = [alert for alert in alerts if alert["risk"] == "Informational"]

    logging.info(f"Total Security Alerts: {len(alerts)}")
    logging.info(
        f"High Risk: {len(high_risk)}, Medium Risk: {len(medium_risk)}, Low Risk: {len(low_risk)}, Informational: {len(informational)}")

    # Print details of High and Medium risk alerts
    if high_risk or medium_risk:
        logging.warning(f"High & Medium Risk Issues Found! 🚨")
        for alert in high_risk + medium_risk:
            logging.warning(f"🚨 {alert['alert']} - {alert['risk']}")
            logging.warning(f"🔗 URL: {alert['url']}")
            logging.warning(f"📌 Solution: {alert['solution']}")
            logging.warning("-" * 80)

    # Only fail the test if High or Medium risk vulnerabilities exist
    assert len(high_risk) == 0 and len(
        medium_risk) == 0, "High/Medium security vulnerabilities found! Check ZAP report."
