import time

from pathlib import Path

from market.market_snapshot import build_market_snapshot

from market.market_intelligence import generate_market_intelligence

from infrastructure.logger import logger

from infrastructure.audit import audit_event

from infrastructure.recovery import safe_execute

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
# BUILD SNAPSHOT RUNNER
# ======================================


def main():

    try:

        start_time = time.time()

        logger.info("BUILD MARKET SNAPSHOT STARTED")

        audit_event("SNAPSHOT_START", "Building market intelligence snapshot")

        # ======================================
        # BUILD SNAPSHOT
        # ======================================

        snapshot = safe_execute(build_market_snapshot, IDX_STOCKS)

        # ======================================
        # VALIDATION
        # ======================================

        if not snapshot:

            logger.error("Snapshot generation failed")

            return

        required_keys = [
            "market_status",
            "breadth_score",
            "strongest_sector",
            "market_bias",
        ]

        missing = [key for key in required_keys if key not in snapshot]

        if missing:

            logger.error(f"Snapshot missing keys: " f"{missing}")

            return

        # ======================================
        # GENERATE INTELLIGENCE
        # ======================================

        intelligence = generate_market_intelligence(snapshot)

        # ======================================
        # EXECUTION TIME
        # ======================================

        execution_time = round(time.time() - start_time, 2)

        # ======================================
        # OUTPUT
        # ======================================

        logger.info("=================================")

        logger.info("MARKET SNAPSHOT COMPLETE")

        logger.info(f"Market Status: " f"{snapshot.get('market_status')}")

        logger.info(f"Breadth Score: " f"{snapshot.get('breadth_score')}")

        logger.info(f"Strongest Sector: " f"{snapshot.get('strongest_sector')}")

        logger.info(f"Sector Leader: " f"{snapshot.get('sector_leader')}")

        logger.info(f"Market Bias: " f"{snapshot.get('market_bias')}")

        logger.info(f"Execution Time: " f"{execution_time}s")

        logger.info("=================================")

        # ======================================
        # MARKET COMMENTARY
        # ======================================

        logger.info("")

        logger.info("AI MARKET INTELLIGENCE")

        logger.info("")

        logger.info(intelligence)

        # ======================================
        # AUDIT
        # ======================================

        audit_event(
            "SNAPSHOT_COMPLETE",
            f"Status="
            f"{snapshot.get('market_status')} | "
            f"Bias="
            f"{snapshot.get('market_bias')}",
        )

    except Exception as e:

        logger.error(f"Snapshot Runner Error: {e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
