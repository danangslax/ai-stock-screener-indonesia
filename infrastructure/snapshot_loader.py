import json

from pathlib import Path

# ======================================
# SNAPSHOT PATH
# ======================================

SNAPSHOT_PATH = Path("data") / "snapshots" / "market_snapshot.json"

# ======================================
# LOAD MARKET SNAPSHOT
# ======================================


def load_market_snapshot():

    try:

        if not SNAPSHOT_PATH.exists():

            print("⚠️ Snapshot not found")

            return None

        with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:

            snapshot = json.load(f)

        print("✅ Snapshot loaded")

        return snapshot

    except Exception as e:

        print(f"❌ Snapshot Load Error: " f"{e}")

        return None
