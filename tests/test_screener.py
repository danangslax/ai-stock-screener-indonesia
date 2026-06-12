import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import time

from core.screener import run_screener

from core.market import get_market_status

# ======================================
# TEST MARKET STATUS
# ======================================


def test_market_status():

    print("🌍 Testing market status...")

    market = get_market_status()

    print(f"📊 Market: " f"{market['status']}")

    print(f"📈 Daily Change: " f"{market['change']}%")

    print(f"⚡ RSI: " f"{market['rsi']}")

    print("-" * 50)


# ======================================
# TEST AI SCREENER
# ======================================


def test_ai_screener():

    print("🚀 Testing AI Screener...")

    start_time = time.time()

    # ======================================
    # RUN SCREENER
    # ======================================

    screener_df = run_screener()

    end_time = time.time()

    runtime = round(end_time - start_time, 2)

    # ======================================
    # EMPTY RESULT
    # ======================================

    if screener_df.empty:

        print("⚠️ No stocks passed screening")

        return

    # ======================================
    # SUMMARY
    # ======================================

    print(f"✅ Total results: " f"{len(screener_df)}")

    print(f"⏱ Runtime: " f"{runtime} seconds")

    print("-" * 50)

    # ======================================
    # TOP PICKS
    # ======================================

    print("🏆 TOP PICKS")

    top_results = screener_df.head(10)

    for i, row in top_results.iterrows():

        print(
            f"{i+1}. "
            f"{row['Symbol']} | "
            f"Score: {row['Score']} | "
            f"RSI: {row['RSI']} | "
            f"RR: {row['Risk_Reward']}"
        )

    print("-" * 50)

    # ======================================
    # BEST STOCK
    # ======================================

    top_pick = screener_df.iloc[0]

    print("🔥 BEST STOCK")

    print(f"Symbol: " f"{top_pick['Symbol']}")

    print(f"Price: " f"{top_pick['Price']}")

    print(f"Score: " f"{top_pick['Score']}")

    print(f"RSI: " f"{top_pick['RSI']}")

    print(f"ADX: " f"{top_pick['ADX']}")

    print(f"Stop Loss: " f"{top_pick['Stop_Loss']}")

    print(f"Take Profit: " f"{top_pick['Take_Profit']}")

    print(f"Risk Reward: " f"{top_pick['Risk_Reward']}")

    print(f"Market: " f"{top_pick['Market']}")

    print("-" * 50)


# ======================================
# TEST SCORE DISTRIBUTION
# ======================================


def test_score_distribution():

    print("📊 Testing score distribution...")

    screener_df = run_screener()

    if screener_df.empty:

        print("⚠️ No screening data")

        return

    average_score = round(screener_df["Score"].mean(), 2)

    max_score = screener_df["Score"].max()

    min_score = screener_df["Score"].min()

    print(f"📈 Average Score: " f"{average_score}")

    print(f"🚀 Highest Score: " f"{max_score}")

    print(f"📉 Lowest Score: " f"{min_score}")

    print("-" * 50)


# ======================================
# TEST RISK REWARD QUALITY
# ======================================


def test_risk_reward():

    print("⚖️ Testing risk reward quality...")

    screener_df = run_screener()

    if screener_df.empty:

        print("⚠️ No screener result")

        return

    strong_rr = screener_df[screener_df["Risk_Reward"] >= 2]

    print(f"✅ Stocks with RR >= 2: " f"{len(strong_rr)}")

    if not strong_rr.empty:

        print("\n🏆 BEST RR STOCKS")

        for _, row in strong_rr.head(5).iterrows():

            print(
                f"{row['Symbol']} | "
                f"RR: {row['Risk_Reward']} | "
                f"Score: {row['Score']}"
            )

    print("-" * 50)


# ======================================
# MAIN TEST RUNNER
# ======================================

if __name__ == "__main__":

    print("🚀 RUNNING AI SCREENER TESTS")

    print("=" * 60)

    test_market_status()

    test_ai_screener()

    test_score_distribution()

    test_risk_reward()

    print("=" * 60)

    print("✅ ALL TESTS COMPLETED")
