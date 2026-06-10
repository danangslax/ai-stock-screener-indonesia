from pathlib import Path

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

from core.daily_timeframe import ( 
    analyze_daily_timeframe
)

# ======================================
# BASE DIRECTORY
# ======================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

# ======================================
# WATCHLIST PATH
# ======================================

WATCHLIST_PATH = (
    BASE_DIR
    / "watchlist"
    / "idx_stocks.txt"
)

# ======================================
# LOAD WATCHLIST
# ======================================

with open(

    WATCHLIST_PATH,

    "r",

    encoding="utf-8"
) as f:

    IDX_STOCKS = [

        line.strip()

        for line in f

        if line.strip()
    ]

print(
    f"✅ Total saham: "
    f"{len(IDX_STOCKS)}"
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
            f"🌍 Market Status: "
            f"{market['status']}"
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
                # REQUIRED COLUMNS
                # ======================================

                required_columns = [

                    "RSI",
                    "ATR",
                    "ADX",
                    "EMA20",
                    "EMA50",
                    "EMA200",
                    "MACD",
                    "MACD_SIGNAL",
                    "VOLATILITY",
                    "VOL_MA20",
                    
                ]

                missing_columns = [

                    col

                    for col in required_columns

                    if col not in df.columns
                ]

                if missing_columns:

                    print(
                        f"⚠️ Missing columns "
                        f"{symbol}: "
                        f"{missing_columns}"
                    )

                    continue

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

                adx = float(
                    latest["ADX"]
                )

                volatility = float(
                    latest["VOLATILITY"]
                )

                ema20 = float(
                    latest["EMA20"]
                )

                ema50 = float(
                    latest["EMA50"]
                )

                relative_volume = round(

                    volume
                    /
                    latest["VOL_MA20"],

                    2
                )

                # ======================================
                # NAN VALIDATION
                # ======================================

                if pd.isna(atr):

                    continue

                if pd.isna(adx):

                    continue

                if pd.isna(rsi):

                    continue

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
                # TREND FILTER
                # ======================================

                if ema20 < ema50:

                    continue

                # ======================================
                # ADX FILTER
                # ======================================

                if adx < 20:

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

                    if rsi < 65:

                        continue

                # ======================================
                # CALCULATE SCORE
                # ======================================

                # ======================================
                # DAILY TIMEFRAME ANALYSIS
                # ======================================

                daily_analysis = (
                    analyze_daily_timeframe(df)
                )

                if daily_analysis is None:

                    continue

                # ======================================
                # DAILY TREND FILTER
                # ======================================

                if (

                    daily_analysis["status"]

                    ==

                    "WEAK"
                ):

                    continue

                score = calculate_score(
                    latest,
                    df
                )

                # ======================================
                # DAILY TIMEFRAME BONUS
                # ======================================

                score += int(
                    daily_analysis["score"] * 0.2
                )

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

                risk = (
                    price - stop_loss
                )

                if risk <= 0:

                    continue

                risk_reward = round(

                    (
                        take_profit - price
                    )
                    /
                    risk,

                    2
                )

                # ======================================
                # RISK REWARD BONUS
                # ======================================

                if risk_reward >= 2:

                    score += 5

                # ======================================
                # SCORE LIMIT
                # ======================================

                if score > 100:

                    score = 100

                # ======================================
                # MINIMUM SCORE
                # ======================================

                if score < 70:

                    continue

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

                    "Relative_Volume": (
                        relative_volume
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
                        adx,
                        2
                    ),

                    "Volatility": round(
                        volatility,
                        4
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
                        ema20,
                        2
                    ),

                    "EMA50": round(
                        ema50,
                        2
                    ),

                    "Score": score,

                    "Stop_Loss": stop_loss,

                    "Take_Profit": take_profit,

                    "Risk_Reward": risk_reward,

                    "Market": (
                        market["status"]
                    ),
                    
                    "Daily_Status": (
                        daily_analysis["status"]
                    ),

                    "Daily_Score": (
                        daily_analysis["score"]
                    ),

                })

            except Exception as e:

                print(
                    f"❌ ERROR "
                    f"{symbol}: {e}"
                )

        # ======================================
        # DATAFRAME
        # ======================================

        result_df = pd.DataFrame(
            results
        )

        # ======================================
        # EMPTY RESULT
        # ======================================

        if result_df.empty:

            print(
                "⚠️ No stocks passed "
                "screening"
            )

            return pd.DataFrame()

        # ======================================
        # SORTING
        # ======================================

        result_df = (

            result_df

            .sort_values(

                by=[

                    "Score",

                    "Relative_Volume"
                ],

                ascending=False
            )

            .reset_index(
                drop=True
            )
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