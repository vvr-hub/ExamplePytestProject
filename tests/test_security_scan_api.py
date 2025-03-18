import pytest
import logging


@pytest.mark.security_scan
def test_api_security_scan(zap):
    """Validates API security vulnerabilities detected by OWASP ZAP"""

    # ✅ Start API scan before checking alerts
    zap.start_api_scan()

    # ✅ Fetch security alerts after scan
    alerts = zap.get_alerts()

    # ✅ Categorize vulnerabilities
    high_risk = [alert for alert in alerts if alert.get("risk") == "High"]
    medium_risk = [alert for alert in alerts if alert.get("risk") == "Medium"]

    logging.info(f"Total Security Alerts: {len(alerts)}")
    logging.info(f"High Risk: {len(high_risk)}, Medium Risk: {len(medium_risk)}")

    # ✅ Log details of High & Medium vulnerabilities
    if high_risk or medium_risk:
        logging.warning("⚠️ High/Medium Security Issues Detected!")
        for alert in high_risk + medium_risk:
            logging.warning(f"🚨 {alert.get('alert', 'Unknown Alert')} - {alert.get('risk', 'Unknown Risk')}")
            logging.warning(f"🔗 Affected URL: {alert.get('url', 'Unknown URL')}")
            logging.warning(f"📌 Solution: {alert.get('solution', 'No suggested solution')}")
            logging.warning("-" * 80)

    # ✅ Fail test only if High-Risk vulnerabilities exist
    assert len(high_risk) == 0, "High security vulnerabilities found! Check ZAP report."
