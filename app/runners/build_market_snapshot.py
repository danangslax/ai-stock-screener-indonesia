from screener.screener import IDX_STOCKS

from core.market_snapshot import build_market_snapshot

# ======================================
# BUILD SNAPSHOT RUNNER
# ======================================


def main():

    print("🚀 Building Market Snapshot")

    snapshot = build_market_snapshot(IDX_STOCKS)

    print("")

    print("=================================")

    print("📈 MARKET SNAPSHOT")

    print(f"Market Status: " f"{snapshot.get('market_status')}")

    print(f"Breadth Score: " f"{snapshot.get('breadth_score')}")

    print(f"Strongest Sector: " f"{snapshot.get('strongest_sector')}")

    print(f"Market Bias: " f"{snapshot.get('market_bias')}")

    print("=================================")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
