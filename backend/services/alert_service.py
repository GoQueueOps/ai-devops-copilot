import os
import requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

print(f"Webhook loaded: {WEBHOOK_URL}")

def send_alert(log_text: str, cause: str, fix: str, severity: str):
    if not WEBHOOK_URL:
        print("No webhook URL configured, skipping alert")
        return

    severity_emoji = {
        "low": "🟡",
        "medium": "🟠",
        "high": "🔴",
        "critical": "🚨"
    }.get(severity, "⚠️")

    message = {
        "embeds": [
            {
                "title": f"{severity_emoji} Incident Detected — {severity.upper()}",
                "color": {
                    "low": 16776960,
                    "medium": 16753920,
                    "high": 16711680,
                    "critical": 10038562
                }.get(severity, 16753920),
                "fields": [
                    {
                        "name": "Cause",
                        "value": cause,
                        "inline": False
                    },
                    {
                        "name": "Fix",
                        "value": fix,
                        "inline": False
                    },
                    {
                        "name": "Original Log",
                        "value": f"```{log_text[:200]}```",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "AI DevOps Copilot"
                }
            }
        ]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=message)
        print(f"Discord response status: {response.status_code}")
        print(f"Discord response body: {response.text}")
        response.raise_for_status()
        print(f"Alert sent successfully for severity: {severity}")
    except Exception as e:
        print(f"Failed to send alert: {e}")