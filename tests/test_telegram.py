import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from core.notifier import (

    send_telegram_message,

    format_screener_message,

    format_confirmation_message
)

# ======================================
# TEST SIMPLE MESSAGE
# ======================================

def test_basic_message():

    print(
        "📨 Testing basic Telegram message..."
    )

    response = send_telegram_message(
        "✅ Telegram bot test successful"
    )

    print(response)


# ======================================
# TEST SCREENER MESSAGE
# ======================================

def test_screener_message():

    print(
        "📊 Testing screener message..."
    )

    # ======================================
    # DUMMY DATA
    # ======================================

    top_pick = {

        "Symbol": "BBCA.JK",

        "Price": 9850,

        "Score": 92,

        "RSI": 67.5,

        "Stop_Loss": 9500,

        "Take_Profit": 10500,

        "Risk_Reward": 2.5
    }

    # ======================================
    # FORMAT MESSAGE
    # ======================================

    message = format_screener_message(

        top_pick,

        market_status="BULLISH"
    )

    # ======================================
    # SEND TELEGRAM
    # ======================================

    response = send_telegram_message(
        message
    )

    print(response)


# ======================================
# TEST CONFIRMATION MESSAGE
# ======================================

def test_confirmation_message():

    print(
        "☀️ Testing confirmation message..."
    )

    message = format_confirmation_message(

        "BBCA.JK",

        "STRONG BUY"
    )

    response = send_telegram_message(
        message
    )

    print(response)


# ======================================
# MAIN TEST RUNNER
# ======================================

if __name__ == "__main__":

    print(
        "🚀 Running Telegram Tests..."
    )

    test_basic_message()

    test_screener_message()

    test_confirmation_message()

    print(
        "✅ Telegram tests completed"
    )