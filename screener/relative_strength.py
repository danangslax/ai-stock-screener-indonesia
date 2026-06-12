import pandas as pd

from core.data_loader import load_stock_data

# ======================================
# CALCULATE RELATIVE STRENGTH
# ======================================


def calculate_relative_strength(stock_df, benchmark_symbol="^JKSE"):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if stock_df.empty:

            return None

        if len(stock_df) < 20:

            return None

        # ======================================
        # LOAD IHSG DATA
        # ======================================

        benchmark_df = load_stock_data(benchmark_symbol, period="6mo", interval="1d")

        if benchmark_df.empty:

            return None

        # ======================================
        # ALIGN DATA
        # ======================================

        min_length = min(len(stock_df), len(benchmark_df))

        stock_df = stock_df.tail(min_length)

        benchmark_df = benchmark_df.tail(min_length)

        # ======================================
        # RETURNS
        # ======================================

        stock_return = stock_df["Close"].iloc[-1] / stock_df["Close"].iloc[-20] - 1

        benchmark_return = (
            benchmark_df["Close"].iloc[-1] / benchmark_df["Close"].iloc[-20] - 1
        )

        # ======================================
        # RELATIVE STRENGTH
        # ======================================

        if benchmark_return == 0:

            rs_ratio = 1

        else:

            rs_ratio = round(stock_return / benchmark_return, 2)

        # ======================================
        # RELATIVE PERFORMANCE
        # ======================================

        relative_performance = round((stock_return - benchmark_return) * 100, 2)

        # ======================================
        # STATUS
        # ======================================

        if rs_ratio >= 2:

            status = "MARKET LEADER"

        elif rs_ratio >= 1.0:

            status = "STRONG"

        elif rs_ratio >= 0.8:

            status = "NEUTRAL"

        else:

            status = "WEAK"

        # ======================================
        # RETURN RESULT
        # ======================================

        return {
            "rs_ratio": rs_ratio,
            "stock_return": round(stock_return * 100, 2),
            "benchmark_return": round(benchmark_return * 100, 2),
            "relative_performance": (relative_performance),
            "status": status,
        }

    except Exception as e:

        print(f"RELATIVE STRENGTH ERROR: " f"{e}")

        return None
