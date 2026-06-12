import pandas as pd

from infrastructure.logger import logger

from storage.data_loader import load_stock_data

# ======================================
# CALCULATE RELATIVE STRENGTH
# ======================================


def calculate_relative_strength(
    stock_df, benchmark_symbol="^JKSE", benchmark_df=None, lookback=20
):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if stock_df.empty:

            return None

        if len(stock_df) < lookback:

            return None

        # ======================================
        # LOAD BENCHMARK
        # ======================================

        if benchmark_df is None:

            benchmark_df = load_stock_data(
                benchmark_symbol, period="6mo", interval="1d", use_cache=True
            )

        if benchmark_df.empty:

            return None

        if len(benchmark_df) < lookback:

            return None

        # ======================================
        # ALIGN DATA
        # ======================================

        stock_close = stock_df[["Close"]].copy()

        benchmark_close = benchmark_df[["Close"]].copy()

        benchmark_close.columns = ["Benchmark_Close"]

        merged = pd.merge(
            stock_close, benchmark_close, left_index=True, right_index=True, how="inner"
        )

        # ======================================
        # VALIDATION
        # ======================================

        if len(merged) < lookback:

            return None

        # ======================================
        # RETURNS
        # ======================================

        stock_return = merged["Close"].iloc[-1] / merged["Close"].iloc[-lookback] - 1

        benchmark_return = (
            merged["Benchmark_Close"].iloc[-1]
            / merged["Benchmark_Close"].iloc[-lookback]
            - 1
        )

        # ======================================
        # RELATIVE PERFORMANCE
        # ======================================

        relative_performance = round((stock_return - benchmark_return) * 100, 2)

        # ======================================
        # RS RATIO
        # ======================================

        if benchmark_return == 0:

            rs_ratio = 1

        else:

            rs_ratio = round((1 + stock_return) / (1 + benchmark_return), 2)

        # ======================================
        # STATUS
        # ======================================

        if relative_performance >= 15:

            status = "MARKET LEADER"

        elif relative_performance >= 5:

            status = "STRONG"

        elif relative_performance >= -5:

            status = "NEUTRAL"

        else:

            status = "WEAK"

        # ======================================
        # RESULT
        # ======================================

        result = {
            "rs_ratio": rs_ratio,
            "stock_return": round(stock_return * 100, 2),
            "benchmark_return": round(benchmark_return * 100, 2),
            "relative_performance": (relative_performance),
            "status": status,
            "lookback": lookback,
            "benchmark": (benchmark_symbol),
            "aligned_periods": len(merged),
        }

        return result

    except Exception as e:

        logger.error(f"Relative Strength " f"Error: {e}")

        return None
