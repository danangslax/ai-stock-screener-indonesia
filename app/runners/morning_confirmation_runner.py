from core.confirmation import morning_confirmation

from database.queries import load_screener_history

from core.market import get_market_status

from core.notifier import send_telegram_message, format_confirmation_message

# ======================================
# MORNING CONFIRMATION RUNNER
# ======================================


def main():

    try:

        print("☀️ Running Morning Confirmation...")

        # ======================================
        # MARKET STATUS
        # ======================================

        market = get_market_status()

        print(f"🌍 Market Status: " f"{market['status']}")

        # ======================================
        # LOAD HISTORY
        # ======================================

        history = load_screener_history(limit=10)

        if not history:

            print("⚠️ No screener history found")

            send_telegram_message("⚠️ No screener history found")

            return

        # ======================================
        # PROCESS STOCKS
        # ======================================

        total_processed = 0

        for stock in history:

            try:

                symbol = stock["Symbol"]

                print(f"📊 Confirming: " f"{symbol}")

                # ======================================
                # CONFIRMATION ENGINE
                # ======================================

                confirmation = morning_confirmation(symbol)

                # ======================================
                # FORMAT MESSAGE
                # ======================================

                message = format_confirmation_message(symbol, confirmation)

                # ======================================
                # ADD MARKET INFO
                # ======================================

                message += f"""

🌍 Market:
<b>{market['status']}</b>
"""

                # ======================================
                # SEND TELEGRAM
                # ======================================

                send_telegram_message(message)

                print(f"✅ {symbol}: " f"{confirmation}")

                total_processed += 1

            except Exception as e:

                print(f"❌ Confirmation Error " f"{stock.get('Symbol')}: " f"{e}")

        # ======================================
        # SUMMARY
        # ======================================

        summary_message = f"""
☀️ <b>MORNING CONFIRMATION DONE</b>

📊 Processed:
{total_processed} stocks

🌍 Market:
<b>{market['status']}</b>
"""

        send_telegram_message(summary_message)

        print("✅ Morning confirmation completed")

    except Exception as e:

        print(f"❌ Morning Runner Error: {e}")

        send_telegram_message(f"❌ Morning Confirmation Error:\n{e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
