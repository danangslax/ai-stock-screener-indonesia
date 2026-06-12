import json

from pathlib import Path

from datetime import datetime

from infrastructure.logger import logger

from market.market import get_market_status

from market.market_breadth import analyze_market_breadth

from market.sector_strength import analyze_sector_strength

from analytics.sector_rotation import (
    analyze_sector_rotation,
)

# ======================================
# SNAPSHOT DIRECTORY
# ======================================

SNAPSHOT_DIR = Path("data") / "snapshots"

SNAPSHOT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ======================================
# SNAPSHOT PATH
# ======================================

SNAPSHOT_PATH = SNAPSHOT_DIR / "market_snapshot.json"

# ======================================
# BUILD MARKET SNAPSHOT
# ======================================


def build_market_snapshot(symbols):

    try:

        logger.info("Building Market Snapshot")

        # ======================================
        # MARKET STATUS
        # ======================================

        try:

            market = get_market_status()

        except Exception as e:

            logger.warning(f"Market engine failed: {e}")

            market = {
                "status": "UNKNOWN",
                "change": 0,
            }

        # ======================================
        # MARKET BREADTH
        # ======================================

        try:

            breadth = analyze_market_breadth(symbols)

        except Exception as e:

            logger.warning(f"Breadth engine failed: {e}")

            breadth = None

        # ======================================
        # SECTOR STRENGTH
        # ======================================

        try:

            sector_df = analyze_sector_strength()

        except Exception as e:

            logger.warning(f"Sector engine failed: {e}")

            sector_df = None

        # ======================================
        # SECTOR ROTATION
        # ======================================

        try:

            sector_analysis = analyze_sector_rotation(symbols)

        except Exception as e:

            logger.warning(f"Sector rotation failed: {e}")

            sector_analysis = {}

        # ======================================
        # DEFAULT VALUES
        # ======================================

        strongest_sector = "N/A"

        sector_leader = "N/A"

        sector_score = 0

        # ======================================
        # TOP SECTOR
        # ======================================

        if sector_df is not None and not sector_df.empty:

            top_sector = sector_df.iloc[0]

            strongest_sector = top_sector["Sector"]

            sector_leader = top_sector["Leader"]

            sector_score = float(top_sector["Score"])

        # ======================================
        # OVERRIDE WITH
        # SECTOR ROTATION
        # ======================================

        strongest_sector = sector_analysis.get(
            "strongest_sector",
            strongest_sector,
        )

        # ======================================
        # SECTOR LEADER
        # ======================================

        sector_leaders = sector_analysis.get(
            "sector_leaders",
            {},
        )

        if strongest_sector in sector_leaders:

            sector_leader = sector_leaders[strongest_sector]["symbol"]

        # ======================================
        # MARKET BIAS
        # ======================================

        market_bias = "DEFENSIVE"

        if breadth:

            health_score = breadth.get(
                "health_score",
                0,
            )

            # ======================================
            # AGGRESSIVE
            # ======================================

            if health_score >= 75 and market["status"] in [
                "STRONG_BULL",
                "BULL",
            ]:

                market_bias = "AGGRESSIVE"

            # ======================================
            # BULLISH
            # ======================================

            elif health_score >= 60:

                market_bias = "BULLISH"

            # ======================================
            # SELECTIVE
            # ======================================

            elif health_score >= 40:

                market_bias = "SELECTIVE"

            # ======================================
            # DEFENSIVE
            # ======================================

            else:

                market_bias = "DEFENSIVE"

        # ======================================
        # SNAPSHOT
        # ======================================

        snapshot = {
            # ======================================
            # BASIC INFO
            # ======================================
            "created_at": str(datetime.now()),
            "snapshot_version": "2.0",
            # ======================================
            # MARKET STATUS
            # ======================================
            "market_status": (
                market.get(
                    "status",
                    "UNKNOWN",
                )
            ),
            "market_change": (
                market.get(
                    "change",
                    0,
                )
            ),
            # ======================================
            # MARKET BREADTH
            # ======================================
            "breadth_score": (
                breadth.get(
                    "health_score",
                    0,
                )
                if breadth
                else 0
            ),
            "breadth_status": (
                breadth.get(
                    "status",
                    "UNKNOWN",
                )
                if breadth
                else "UNKNOWN"
            ),
            # ======================================
            # SECTOR ANALYSIS
            # ======================================
            "strongest_sector": (strongest_sector),
            "sector_leader": (sector_leader),
            "sector_score": (sector_score),
            "sector_scores": (
                sector_analysis.get(
                    "sector_scores",
                    {},
                )
            ),
            "sector_leaders": (
                sector_analysis.get(
                    "sector_leaders",
                    {},
                )
            ),
            "top_stocks_by_sector": (
                sector_analysis.get(
                    "top_stocks_by_sector",
                    {},
                )
            ),
            # ======================================
            # MARKET BIAS
            # ======================================
            "market_bias": (market_bias),
            # ======================================
            # METADATA
            # ======================================
            "total_symbols": len(symbols),
        }

        logger.info("Market Snapshot Ready")

        # ======================================
        # SAVE SNAPSHOT
        # ======================================

        with open(
            SNAPSHOT_PATH,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                snapshot,
                f,
                indent=4,
                default=str,
                ensure_ascii=False,
            )

        logger.info("Snapshot saved")

        return snapshot

    except Exception as e:

        logger.error(f"Snapshot Error: {e}")

        return {
            "market_status": "UNKNOWN",
            "breadth_score": 0,
            "strongest_sector": "N/A",
            "sector_leader": "N/A",
            "market_bias": "DEFENSIVE",
            "sector_scores": {},
            "sector_leaders": {},
            "top_stocks_by_sector": {},
        }
