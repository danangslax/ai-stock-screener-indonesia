import pandas as pd

from core.data_loader import (
    load_stock_data
)

from core.indicators import (
    add_indicators
)

from core.scoring import (
    calculate_score
)

from core.market import (
    get_market_status
)

# ======================================
# LOAD WATCHLIST
# ======================================

with open("watchlist/idx_stocks.txt") as f:

    IDX_STOCKS = [

        line.strip()

        for line in f

        if line.strip()
    ]

print(
    f"✅ Total saham: {len(IDX_STOCKS)}"
)

# ======================================
# AI SCREENER ENGINE
# ======================================

def run_screener():

    try:

        # ======================================
        # MARKET STATUS
        # ======================================

        market = get_market_status()

        print(
            f"🌍 Market: {market['status']}"
        )

        # ======================================
        # RESULT CONTAINER
        # ======================================

        results = []

        total = len(IDX_STOCKS)

        # ======================================
        # LOOP STOCKS
        # ======================================

        for i, symbol in enumerate(
            IDX_STOCKS
        ):

            print(
                f"📊 Scanning "
                f"{i+1}/{total}: "
                f"{symbol}"
            )

            try:

                # ======================================
                # LOAD DATA
                # ======================================

                df = load_stock_data(
                    symbol,
                    period="6mo",
                    interval="1d"
                )

                # ======================================
                # VALIDATION
                # ======================================

                if df.empty:

                    continue

                if len(df) < 60:

                    continue

                # ======================================
                # ADD INDICATORS
                # ======================================

                df = add_indicators(df)

                if df.empty:

                    continue

                latest = df.iloc[-1]

                # ======================================
                # BASIC DATA
                # ======================================

                price = float(
                    latest["Close"]
                )

                volume = float(
                    latest["Volume"]
                )

                value = (
                    price * volume
                )

                rsi = float(
                    latest["RSI"]
                )

                atr = float(
                    latest["ATR"]
                )

                volatility = float(
                    latest["VOLATILITY"]
                )

                # ======================================
                # BASIC FILTER
                # ======================================

                # Avoid gocap
                if price < 50:

                    continue

                # Avoid expensive stocks
                if price > 5000:

                    continue

                # Minimum liquidity
                if volume < 1_000_000:

                    continue

                # Minimum transaction value
                if value < 15_000_000_000:

                    continue

                # ======================================
                # VOLATILITY FILTER
                # ======================================

                if volatility > 0.15:

                    continue

                # ======================================
                # RSI FILTER
                # ======================================

                if rsi < 50:

                    continue

                # Avoid overbought
                if rsi > 85:

                    continue

                # ======================================
                # MARKET FILTER
                # ======================================

                if (
                    market["status"]
                    == "STRONG BEARISH"
                ):

                    # only strongest setups
                    if rsi < 65:

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

                if score < 70:

                    continue

                # ======================================
                # TRADE PLAN
                # ======================================

                stop_loss = round(
                    price - (2 * atr),
                    2
                )

                take_profit = round(
                    price + (4 * atr),
                    2
                )

                risk_reward = round(
                    (
                        take_profit - price
                    )
                    /
                    (
                        price - stop_loss
                    ),
                    2
                )

                # ======================================
                # SAVE RESULT
                # ======================================

                results.append({

                    "Symbol": symbol,

                    "Price": round(
                        price,
                        2
                    ),

                    "Volume": int(
                        volume
                    ),

                    "Value": int(
                        value
                    ),

                    "RSI": round(
                        rsi,
                        2
                    ),

                    "ATR": round(
                        atr,
                        2
                    ),

                    "ADX": round(
                        latest["ADX"],
                        2
                    ),

                    "MA5": round(
                        latest["MA5"],
                        2
                    ),

                    "MA20": round(
                        latest["MA20"],
                        2
                    ),

                    "EMA20": round(
                        latest["EMA20"],
                        2
                    ),

                    "EMA50": round(
                        latest["EMA50"],
                        2
                    ),

                    "Score": score,

                    "Stop_Loss": stop_loss,

                    "Take_Profit": take_profit,

                    "Risk_Reward": risk_reward,

                    "Market": market["status"]
                })

            except Exception as e:

                print(
                    f"❌ ERROR {symbol}: {e}"
                )

        # ======================================
        # DATAFRAME
        # ======================================

        result_df = pd.DataFrame(
            results
        )

        # ======================================
        # SORTING
        # ======================================

        if not result_df.empty:

            result_df = (
                result_df
                .sort_values(
                    by="Score",
                    ascending=False
                )
                .reset_index(drop=True)
            )

            # ======================================
            # TOP RESULTS
            # ======================================

            result_df = result_df.head(50)

        print(
            f"✅ Total results: "
            f"{len(result_df)}"
        )

        return result_df

    except Exception as e:

        print(
            f"❌ Screener Error: {e}"
        )

        return pd.DataFrame()
