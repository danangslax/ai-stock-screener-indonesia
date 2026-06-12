import time
import pandas as pd

from pathlib import Path

from screener.screener import run_screener

from market.market import get_market_status

from market.market_snapshot import build_market_snapshot

from ai.market_commentary import generate_market_commentary

from infrastructure.logger import logger

from infrastructure.audit import audit_event

from infrastructure.recovery import safe_execute

from infrastructure.notifier import send_telegram_message, format_screener_message

from database.queries import save_screener_results

# ======================================
# WATCHLIST
# ======================================

WATCHLIST_PATH = Path("watchlist") / "idx_stocks.txt"

with open(
    WATCHLIST_PATH,
    "r",
    encoding="utf-8",
) as f:

    IDX_STOCKS = [line.strip() for line in f if line.strip()]

# ======================================
# AI SCREENER ENGINE
# ======================================


def main():

    try:

        start_time = time.time()

        logger.info("AI SCREENER STARTED")

        audit_event("SCREENER_START", "AI Screener execution")

        # ======================================
        # MARKET STATUS
        # ======================================

        market = safe_execute(get_market_status)

        if not market:

            logger.error("Market status unavailable")

            return

        logger.info(f"Market Status: " f"{market['status']}")

        # ======================================
        # RUN SCREENER
        # ======================================

        screener_result = safe_execute(run_screener)

        if not screener_result:

            logger.error("Screener execution failed")

            return

        screener_df, filtered_symbols = screener_result

        # ======================================
        # EMPTY RESULT
        # ======================================

        if screener_df is None:

            screener_df = pd.DataFrame()

        # ======================================
        # BUILD SNAPSHOT
        # ======================================

        snapshot = safe_execute(build_market_snapshot, filtered_symbols)

        if not snapshot:

            logger.warning("Snapshot unavailable")

            snapshot = {
                "market_status": (market["status"]),
                "breadth_score": 0,
                "strongest_sector": "N/A",
                "sector_leader": "N/A",
                "market_bias": "DEFENSIVE",
            }

        # ======================================
        # MARKET COMMENTARY
        # ======================================

        commentary = generate_market_commentary(snapshot, screener_df)

        # ======================================
        # NO SIGNAL FOUND
        # ======================================

        if screener_df.empty:

            logger.warning("No stock passed screening")

            empty_message = f"""
⚠️ <b>AI SCREENER</b>

No stock passed today's screening.

🌍 Market:
{market['status']}

🎯 Bias:
{snapshot['market_bias']}
"""

            safe_execute(send_telegram_message, empty_message)

            safe_execute(send_telegram_message, commentary)

            return

        # ======================================
        # VALIDATE SIGNALS
        # ======================================

        required_columns = [
            "Symbol",
            "Price",
            "Confidence",
            "Strategy",
        ]

        missing_columns = [
            col for col in required_columns if col not in screener_df.columns
        ]

        if missing_columns:

            logger.error(f"Missing screener columns: " f"{missing_columns}")

            return

        # ======================================
        # SORT BEST SIGNALS
        # ======================================

        screener_df = screener_df.sort_values(
            by="Confidence", ascending=False
        ).reset_index(drop=True)

        # ======================================
        # TOP PICK
        # ======================================

        top_pick = screener_df.iloc[0]

        logger.info(f"Top Pick: " f"{top_pick['Symbol']}")

        # ======================================
        # CONFIDENCE METRICS
        # ======================================

        average_confidence = round(screener_df["Confidence"].mean(), 2)

        highest_confidence = round(screener_df["Confidence"].max(), 2)

        signal_count = len(screener_df)

        # ======================================
        # SAVE DATABASE
        # ======================================

        logger.info("Saving screener results")

        safe_execute(save_screener_results, screener_df)

        # ======================================
        # TELEGRAM MESSAGE
        # ======================================

        message = format_screener_message(top_pick, market["status"])

        # ======================================
        # SEND SIGNAL
        # ======================================

        safe_execute(send_telegram_message, message)

        # ======================================
        # SEND COMMENTARY
        # ======================================

        safe_execute(send_telegram_message, commentary)

        # ======================================
        # EXECUTION METRICS
        # ======================================

        execution_time = round(time.time() - start_time, 2)

        # ======================================
        # HEALTH STATUS
        # ======================================

        health_status = "HEALTHY"

        if average_confidence < 65:

            health_status = "WARNING"

        if average_confidence < 50:

            health_status = "WEAK"

        # ======================================
        # FINAL SUMMARY
        # ======================================

        logger.info("=================================")

        logger.info("AI SCREENER COMPLETE")

        logger.info(f"Signals: " f"{signal_count}")

        logger.info(f"Average Confidence: " f"{average_confidence}")

        logger.info(f"Highest Confidence: " f"{highest_confidence}")

        logger.info(f"Execution Time: " f"{execution_time}s")

        logger.info(f"Health Status: " f"{health_status}")

        logger.info("=================================")

        # ======================================
        # AUDIT EVENT
        # ======================================

        audit_event(
            "SCREENER_COMPLETE",
            f"Signals={signal_count} | "
            f"Top={top_pick['Symbol']} | "
            f"Health={health_status}",
        )

    except Exception as e:

        logger.error(f"Auto Screener Error: {e}")

        safe_execute(send_telegram_message, f"❌ AI Screener Error:\n{e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
