import os
import requests

from dotenv import load_dotenv

# ======================================
# LOAD ENV
# ======================================

load_dotenv()

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

# ======================================
# SEND TELEGRAM MESSAGE
# ======================================

def send_telegram_message(message):

    try:

        url = (
            f"https://api.telegram.org/bot"
            f"{BOT_TOKEN}/sendMessage"
        )

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(
            url,
            json=payload
        )

        return response.json()

    except Exception as e:

        print("Telegram Error:", e)