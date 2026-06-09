from core.screener import run_screener
from database.queries import (
    save_screener_results
)
from core.notifier import (
    send_telegram_message
)

# ======================================
# RUN SCREENER
# ======================================

print("Running AI Screener...")

screener_df = run_screener()

# ======================================
# CHECK RESULT
# ======================================

if screener_df.empty:

    print("No stocks found")

    send_telegram_message(
        "⚠️ No stock passed screening today"
    )

else:

    print("Saving results...")

    save_screener_results(
        screener_df
    )

    # ======================================
    # TOP PICK
    # ======================================

    top_pick = screener_df.iloc[0]

    message = f"""
🔥 NIGHTLY AI SCREENER

Top Pick:
{top_pick["Symbol"]}

Score: {top_pick["Score"]}
RSI: {top_pick["RSI"]}

AI breakout detected
"""

    print(message)

    send_telegram_message(message)

    print("Done.")