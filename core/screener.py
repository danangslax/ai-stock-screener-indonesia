import yfinance as yf
import pandas as pd

from core.indicators import add_indicators
from core.scoring import calculate_score

# ======================================
# LOAD WATCHLIST
# ======================================

with open("watchlist/idx_stocks.txt") as f:

    IDX_STOCKS = [
        line.strip()
        for line in f
        if line.strip()
    ]

print(f"Total saham: {len(IDX_STOCKS)}")

# ======================================
# SCREENER ENGINE
# ======================================

def run_screener():

    results = []

    total = len(IDX_STOCKS)

    for i, symbol in enumerate(IDX_STOCKS):

        print(
            f"Scanning {i+1}/{total}: {symbol}"
        )

        try:

            # ======================================
            # DOWNLOAD DATA
            # ======================================

            df = yf.download(
                symbol,
                period="3mo",
                interval="1d",
                auto_adjust=True,
                progress=False
            )

            # ======================================
            # FIX MULTI INDEX
            # ======================================

            if isinstance(df.columns, pd.MultiIndex):

                df.columns = (
                    df.columns.get_level_values(0)
                )

            # ======================================
            # VALIDATION
            # ======================================

            if df.empty:
                continue

            if len(df) < 30:
                continue

            # ======================================
            # ADD INDICATORS
            # ======================================

            df = add_indicators(df)

            latest = df.iloc[-1]

            price = latest["Close"]

            volume = latest["Volume"]

            value = price * volume

            # ======================================
            # BASIC FILTER
            # ======================================

            if price < 50:
                continue

            if price > 500:
                continue

            if volume < 1_000_000:
                continue

            if value < 15_000_000_000:
                continue

            # ======================================
            # CALCULATE SCORE
            # ======================================

            score = calculate_score(
                latest,
                df
            )

            # ======================================
            # MINIMUM SCORE
            # ======================================

            if score < 60:
                continue

            # ======================================
            # SAVE RESULT
            # ======================================

            results.append({

                "Symbol": symbol,

                "Price": round(price, 2),

                "Volume": int(volume),

                "Value": int(value),

                "RSI": round(
                    latest["RSI"], 2
                ),

                "MA5": round(
                    latest["MA5"], 2
                ),

                "MA20": round(
                    latest["MA20"], 2
                ),

                "Score": score
            })

        except Exception as e:

            print(
                f"ERROR {symbol}: {e}"
            )

    # ======================================
    # DATAFRAME
    # ======================================

    result_df = pd.DataFrame(results)

    # ======================================
    # SORTING
    # ======================================

    if not result_df.empty:

        result_df = result_df.sort_values(
            by="Score",
            ascending=False
        )

        # TOP RESULTS
        result_df = result_df.head(50)

    return result_df