import os

import requests

from dotenv import load_dotenv

from infrastructure.logger import logger

# ======================================
# LOAD ENVIRONMENT VARIABLES
# ======================================

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ======================================
# VALIDATION
# ======================================

if not BOT_TOKEN:

    logger.warning("TELEGRAM_BOT_TOKEN missing")

if not CHAT_ID:

    logger.warning("TELEGRAM_CHAT_ID missing")

# ======================================
# SEND TELEGRAM MESSAGE
# ======================================


def send_telegram_message(message, parse_mode="HTML"):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not BOT_TOKEN:

            return {"status": "error", "message": ("Missing Telegram token")}

        if not CHAT_ID:

            return {"status": "error", "message": ("Missing Telegram chat id")}

        # ======================================
        # TELEGRAM API URL
        # ======================================

        url = f"https://api.telegram.org/bot" f"{BOT_TOKEN}/sendMessage"

        # ======================================
        # PAYLOAD
        # ======================================

        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": parse_mode}

        # ======================================
        # SEND REQUEST
        # ======================================

        response = requests.post(url, json=payload, timeout=15)

        result = response.json()

        # ======================================
        # SUCCESS
        # ======================================

        if response.status_code == 200 and result.get("ok"):

            logger.info("Telegram message sent")

            return result

        # ======================================
        # FAILED
        # ======================================

        logger.error(f"Telegram API Error: " f"{result}")

        return {"status": "error", "message": result}

    except requests.Timeout:

        logger.error("Telegram timeout")

        return {"status": "error", "message": "timeout"}

    except Exception as e:

        logger.error(f"Telegram Error: {e}")

        return {"status": "error", "message": str(e)}


# ======================================
# FORMAT NIGHT SCREENER MESSAGE
# ======================================


def format_screener_message(top_pick, market_status=None):

    try:

        symbol = top_pick["Symbol"]

        price = top_pick["Price"]

        score = top_pick["Score"]

        rsi = top_pick["RSI"]

        stop_loss = top_pick["Stop_Loss"]

        take_profit = top_pick["Take_Profit"]

        rr = top_pick["Risk_Reward"]

        market = market_status or "UNKNOWN"

        message = f"""
🔥 <b>NIGHTLY AI SCREENER</b>

🏆 <b>Top Pick:</b>
{symbol}

💰 Price: {price}
📊 Score: {score}
⚡ RSI: {rsi}

🛑 Stop Loss: {stop_loss}
🎯 Take Profit: {take_profit}

⚖️ Risk Reward: {rr}

🌍 Market: {market}

🤖 AI breakout detected
"""

        return message

    except Exception as e:

        logger.error(f"Format Error: {e}")

        return "❌ Failed to format message"


# ======================================
# FORMAT MORNING CONFIRMATION
# ======================================


def format_confirmation_message(symbol, confirmation):

    try:

        emoji = "👀"

        if confirmation == "STRONG BUY":

            emoji = "🚀"

        elif confirmation == "BUY":

            emoji = "✅"

        elif confirmation == "AVOID":

            emoji = "❌"

        elif confirmation == "WEAK":

            emoji = "⚠️"

        message = f"""
☀️ <b>MORNING CONFIRMATION</b>

{emoji} {symbol}

📌 Status:
<b>{confirmation}</b>
"""

        return message

    except Exception as e:

        logger.error(f"Confirmation Format " f"Error: {e}")

        return "❌ Failed to format confirmation"
