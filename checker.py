python
import os
import sys
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://cbseresults.nic.in/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def send_telegram(message):
    response = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )
    response.raise_for_status()


try:
    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    html = response.text.lower()

    if "will be available soon" in html:
        print("Results not yet declared.")
        sys.exit(0)

    # Phrase disappeared → likely results are out
    send_telegram(
        "🚨 CBSE Class 10 Second Board 2026 results may have been declared!\n\n"
        f"Check here: {URL}"
    )

    print("Notification sent successfully!")

    # Exit with special code so GitHub can disable the workflow
    sys.exit(10)

except Exception as e:
    print("Error:", e)
    sys.exit(1)
