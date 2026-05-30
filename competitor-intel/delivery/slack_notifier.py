import requests
from config import SLACK_WEBHOOK_URL

def send_to_slack(summary):
    if not SLACK_WEBHOOK_URL:
        print("\n--- WEEKLY COMPETITOR DIGEST ---\n")
        print(summary)
        print("\n--- END DIGEST ---\n")
        return

    payload = {
        "text": f"*Weekly Competitor Intelligence Digest*\n\n{summary}"
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("Sent to Slack successfully")
    else:
        print(f"Slack error: {response.status_code}")