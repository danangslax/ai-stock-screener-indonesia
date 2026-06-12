from screener.screener import IDX_STOCKS, run_screener

from core.market import get_market_status

from database.queries import save_screener_results

from core.notifier import send_telegram_message, format_screener_message

from core.market_commentary import generate_market_commentary

from core.market_snapshot import build_market_snapshot

# ======================================
# RUN AI SCREENER
# ======================================


def main():

    try:

        print("🚀 Running AI Screener...")

        # ======================================
        # MARKET STATUS
        # ======================================

        market = get_market_status()

        print(f"🌍 Market Status: " f"{market['status']}")

        # ======================================
        # RUN SCREENER
        # ======================================

        screener_df, filtered_symbols = run_screener()

        # ======================================
        # BUILD MARKET SNAPSHOT
        # ======================================

        snapshot = build_market_snapshot(filtered_symbols)

        # ======================================
        # AI MARKET COMMENTARY
        # ======================================

        commentary = generate_market_commentary(snapshot, screener_df)

        # ======================================
        # EMPTY RESULT
        # ======================================

        if screener_df.empty:

            print("⚠️ No stocks found")

            message = f"""
⚠️ <b>AI SCREENER</b>

No stock passed today's screening.

🌍 Market:
{market['status']}
"""

            send_telegram_message(message)

            # ======================================
            # SEND COMMENTARY
            # ======================================

            send_telegram_message(commentary)

            return

        # ======================================
        # SAVE DATABASE
        # ======================================

        print("💾 Saving screener results...")

        save_screener_results(screener_df)

        # ======================================
        # TOP PICK
        # ======================================

        top_pick = screener_df.iloc[0]

        print(f"🏆 Top Pick: " f"{top_pick['Symbol']}")

        # ======================================
        # FORMAT MESSAGE
        # ======================================

        message = format_screener_message(top_pick, market["status"])

        # ======================================
        # SEND TOP PICK
        # ======================================

        send_telegram_message(message)

        # ======================================
        # SEND MARKET COMMENTARY
        # ======================================

        send_telegram_message(commentary)

        print("✅ Screener completed")

    except Exception as e:

        print(f"❌ Auto Screener Error: {e}")

        send_telegram_message(f"❌ AI Screener Error:\n{e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
