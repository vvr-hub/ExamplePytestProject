import pytest
import logging
import sys

should_run_explicitly = any(
    arg.endswith("test_security_scan_api.py") or "test_api_security_scan" in arg
    for arg in sys.argv
)


@pytest.mark.security_scan
@pytest.mark.skipif(not should_run_explicitly, reason="Skipped by default. Run explicitly to execute OWASP ZAP test.")
def test_api_security_scan(zap):
    """Validates API security vulnerabilities detected by OWASP ZAP"""

    zap.start_api_scan()

    alerts = zap.get_alerts()
    high_risk = [alert for alert in alerts if alert.get("risk") == "High"]
    medium_risk = [alert for alert in alerts if alert.get("risk") == "Medium"]

    logging.info(f"Total Security Alerts: {len(alerts)}")
    logging.info(f"High Risk: {len(high_risk)}, Medium Risk: {len(medium_risk)}")

    if high_risk or medium_risk:
        logging.warning("⚠️ High/Medium Security Issues Detected!")
        for alert in high_risk + medium_risk:
            logging.warning(f"🚨 {alert.get('alert', 'Unknown Alert')} - {alert.get('risk', 'Unknown Risk')}")
            logging.warning(f"🔗 Affected URL: {alert.get('url', 'Unknown URL')}")
            logging.warning(f"📌 Solution: {alert.get('solution', 'No suggested solution')}")
            logging.warning("-" * 80)

    assert len(high_risk) == 0, "High security vulnerabilities found! Check ZAP report."
