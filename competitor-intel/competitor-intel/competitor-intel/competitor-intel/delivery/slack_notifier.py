import requests
from config import SLACK_WEBHOOK_URL

def send_to_slack(summary):
    if not SLACK_WEBHOOK_URL:
        print("No Slack webhook configured. Printing to console instead:")
        print(summary)
        return

    payload = {
        "text": f"*Weekly Competitor Intelligence Digest*\n\n{summary}"
    }

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("Digest sent to Slack successfully")
    else:
        print(f"Failed to send to Slack: {response.status_code}")