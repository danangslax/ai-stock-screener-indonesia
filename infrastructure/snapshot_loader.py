import json

from pathlib import Path

from infrastructure.logger import logger

# ======================================
# SNAPSHOT DIRECTORY
# ======================================

SNAPSHOT_DIR = Path("data") / "snapshots"

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# SNAPSHOT PATH
# ======================================

SNAPSHOT_PATH = SNAPSHOT_DIR / "market_snapshot.json"

# ======================================
# DEFAULT SNAPSHOT
# ======================================

DEFAULT_SNAPSHOT = {
    "market_status": "UNKNOWN",
    "market_bias": "DEFENSIVE",
    "breadth_score": 0,
    "breadth_status": "UNKNOWN",
    "strongest_sector": "N/A",
    "sector_leader": "N/A",
    "sector_score": 0,
}

# ======================================
# LOAD MARKET SNAPSHOT
# ======================================


def load_market_snapshot():

    try:

        # ======================================
        # FILE EXISTS
        # ======================================

        if not SNAPSHOT_PATH.exists():

            logger.warning("Snapshot not found")

            return DEFAULT_SNAPSHOT

        # ======================================
        # LOAD JSON
        # ======================================

        with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:

            snapshot = json.load(f)

        # ======================================
        # VALIDATION
        # ======================================

        required_keys = [
            "market_status",
            "market_bias",
            "breadth_score",
            "strongest_sector",
        ]

        missing = [key for key in required_keys if key not in snapshot]

        if missing:

            logger.warning(f"Snapshot missing keys: " f"{missing}")

            return DEFAULT_SNAPSHOT

        logger.info("Market snapshot loaded")

        return snapshot

    except Exception as e:

        logger.error(f"Snapshot Load Error: " f"{e}")

        return DEFAULT_SNAPSHOT
