from core.screener import (
    run_screener
)

from core.market import (
    get_market_status
)

from database.queries import (
    save_screener_results
)

from core.notifier import (

    send_telegram_message,

    format_screener_message
)

# ======================================
# RUN AI SCREENER
# ======================================

def main():

    try:

        print(
            "🚀 Running AI Screener..."
        )

        # ======================================
        # MARKET STATUS
        # ======================================

        market = get_market_status()

        print(
            f"🌍 Market Status: "
            f"{market['status']}"
        )

        # ======================================
        # RUN SCREENER
        # ======================================

        screener_df = run_screener()

        # ======================================
        # EMPTY RESULT
        # ======================================

        if screener_df.empty:

            print(
                "⚠️ No stocks found"
            )

            message = f"""
⚠️ <b>AI SCREENER</b>

No stock passed today's screening.

🌍 Market:
{market['status']}
"""

            send_telegram_message(
                message
            )

            return

        # ======================================
        # SAVE DATABASE
        # ======================================

        print(
            "💾 Saving screener results..."
        )

        save_screener_results(
            screener_df
        )

        # ======================================
        # TOP PICK
        # ======================================

        top_pick = screener_df.iloc[0]

        print(
            f"🏆 Top Pick: "
            f"{top_pick['Symbol']}"
        )

        # ======================================
        # FORMAT MESSAGE
        # ======================================

        message = format_screener_message(

            top_pick,

            market["status"]
        )

        # ======================================
        # SEND TELEGRAM
        # ======================================

        send_telegram_message(
            message
        )

        print(
            "✅ Screener completed"
        )

    except Exception as e:

        print(
            f"❌ Auto Screener Error: {e}"
        )

        send_telegram_message(
            f"❌ AI Screener Error:\n{e}"
        )


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()