from core.trade_audit import (
    run_trade_audit
)

from core.notifier import (
    send_telegram_message
)

from core.paper_trading import (
    load_open_trades
)

# ======================================
# TRADE AUDIT RUNNER
# ======================================

def main():

    try:

        print(
            "📊 Running Trade Audit..."
        )

        # ======================================
        # LOAD OPEN TRADES
        # ======================================

        open_trades = load_open_trades()

        total_open = len(open_trades)

        print(
            f"📂 Open trades: "
            f"{total_open}"
        )

        # ======================================
        # NO OPEN TRADES
        # ======================================

        if total_open == 0:

            message = """
📊 <b>TRADE AUDIT</b>

⚠️ No open trades found.
"""

            send_telegram_message(
                message
            )

            print(
                "⚠️ No open trades"
            )

            return

        # ======================================
        # RUN AUDIT ENGINE
        # ======================================

        run_trade_audit()

        # ======================================
        # SUMMARY
        # ======================================

        summary_message = f"""
📊 <b>TRADE AUDIT COMPLETED</b>

✅ Total open trades checked:
{total_open}

🤖 Audit engine finished successfully.
"""

        send_telegram_message(
            summary_message
        )

        print(
            "✅ Trade audit completed"
        )

    except Exception as e:

        print(
            f"❌ Trade Audit Runner Error: {e}"
        )

        send_telegram_message(
            f"❌ Trade Audit Error:\n{e}"
        )


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()