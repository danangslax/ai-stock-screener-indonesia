import json

from pathlib import Path

from core.market import get_market_status

from core.market_breadth import analyze_market_breadth

from core.sector_strength import analyze_sector_strength

# ======================================
# SNAPSHOT DIRECTORY
# ======================================

SNAPSHOT_DIR = Path("data") / "snapshots"

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# BUILD MARKET SNAPSHOT
# ======================================


def build_market_snapshot(symbols):

    try:

        print("📈 Building Market Snapshot")

        # ======================================
        # MARKET STATUS
        # ======================================

        market = get_market_status()

        # ======================================
        # MARKET BREADTH
        # ======================================

        breadth = analyze_market_breadth(symbols)

        # ======================================
        # SECTOR STRENGTH
        # ======================================

        sector_df = analyze_sector_strength()

        # ======================================
        # DEFAULT VALUES
        # ======================================

        strongest_sector = "N/A"

        sector_leader = "N/A"

        sector_score = 0

        # ======================================
        # TOP SECTOR
        # ======================================

        if not sector_df.empty:

            top_sector = sector_df.iloc[0]

            strongest_sector = top_sector["Sector"]

            sector_leader = top_sector["Leader"]

            sector_score = top_sector["Score"]

        # ======================================
        # MARKET BIAS
        # ======================================

        market_bias = "DEFENSIVE"

        if breadth:

            health_score = breadth["health_score"]

            if health_score >= 75:

                market_bias = "AGGRESSIVE"

            elif health_score >= 60:

                market_bias = "BULLISH"

            elif health_score >= 40:

                market_bias = "SELECTIVE"

            else:

                market_bias = "DEFENSIVE"

        # ======================================
        # SNAPSHOT RESULT
        # ======================================

        snapshot = {
            "market_status": (market["status"]),
            "market_change": (market.get("change", 0)),
            "breadth_score": (breadth.get("health_score", 0) if breadth else 0),
            "breadth_status": (
                breadth.get("status", "UNKNOWN") if breadth else "UNKNOWN"
            ),
            "strongest_sector": (strongest_sector),
            "sector_leader": (sector_leader),
            "sector_score": (sector_score),
            "market_bias": (market_bias),
        }

        print("✅ Market Snapshot Ready")

        # ======================================
        # SAVE SNAPSHOT
        # ======================================

        snapshot_path = SNAPSHOT_DIR / "market_snapshot.json"

        with open(snapshot_path, "w", encoding="utf-8") as f:

            json.dump(snapshot, f, indent=4, default=str)

        print("💾 Snapshot saved")

        return snapshot

    except Exception as e:

        print(f"❌ Snapshot Error: " f"{e}")

        return {
            "market_status": "UNKNOWN",
            "breadth_score": 0,
            "strongest_sector": "N/A",
            "market_bias": "DEFENSIVE",
        }
