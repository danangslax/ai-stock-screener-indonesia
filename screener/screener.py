from pathlib import Path

import pandas as pd

from core.data_loader import load_stock_data

from core.scoring import calculate_score

from core.market import get_market_status

from core.daily_timeframe import analyze_daily_timeframe

from core.relative_strength import calculate_relative_strength

from core.universe_filter import filter_universe

from core.strategy_router import run_strategy

from core.weekly_timeframe import analyze_weekly_timeframe

from core.confidence import calculate_confidence

from core.meta_strategy import adjust_confidence

from core.trade_journal import load_journal

from core.learning_engine import analyze_learning_data

from core.ai_parameters import load_parameters

from app.services.infrastructure.logger import logger

# ======================================
# BASE DIRECTORY
# ======================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================
# WATCHLIST PATH
# ======================================

WATCHLIST_PATH = BASE_DIR / "watchlist" / "idx_stocks.txt"

# ======================================
# LOAD WATCHLIST
# ======================================

with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:

    IDX_STOCKS = [line.strip() for line in f if line.strip()]

print(f"✅ Total saham: " f"{len(IDX_STOCKS)}")

# ======================================
# AI SCREENER ENGINE
# ======================================


def run_screener():

    filtered_symbols = []

    try:

        # ======================================
        # MARKET STATUS
        # ======================================

        market = get_market_status()

        logger.info(f"Market Status: " f"{market['status']}")

        # ======================================
        # LOAD AI PARAMETERS
        # ======================================

        ai_parameters = load_parameters()

        min_rsi = ai_parameters["min_rsi"]

        min_adx = ai_parameters["min_adx"]

        max_volatility = ai_parameters["max_volatility"]

        print(
            f"🤖 AI Parameters | "
            f"RSI: {min_rsi} | "
            f"ADX: {min_adx} | "
            f"VOL: {max_volatility}"
        )

        # ======================================
        # LOAD AI LEARNING
        # ======================================

        journal_data = load_journal()

        learning_df = analyze_learning_data(journal_data)

        # ======================================
        # RESULT CONTAINER
        # ======================================

        results = []

        # ======================================
        # FAST UNIVERSE FILTER
        # ======================================

        filtered_symbols = filter_universe(IDX_STOCKS)

        total = len(filtered_symbols)

        print(f"🔥 Filtered Universe: " f"{total}")

        # ======================================
        # EMPTY FILTER RESULT
        # ======================================

        if total == 0:

            print("⚠️ Universe filter empty")

            return (pd.DataFrame(), [])

        # ======================================
        # LOOP STOCKS
        # ======================================

        for i, symbol in enumerate(filtered_symbols):

            print(f"📊 Scanning " f"{i+1}/{total}: " f"{symbol}")

            try:

                # ======================================
                # LOAD ENRICHED CACHE
                # ======================================

                df = load_stock_data(symbol, period="6mo", interval="1d")

                # ======================================
                # VALIDATION
                # ======================================

                if df.empty:

                    continue

                if len(df) < 60:

                    continue

                # ======================================
                # VALIDATE INDICATORS
                # ======================================

                if "RSI" not in df.columns:

                    print(f"⚠️ Indicators missing " f"{symbol}")

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
                    col for col in required_columns if col not in df.columns
                ]

                if missing_columns:

                    print(f"⚠️ Missing columns " f"{symbol}: " f"{missing_columns}")

                    continue

                # ======================================
                # BASIC DATA
                # ======================================

                price = float(latest["Close"])

                volume = float(latest["Volume"])

                value = price * volume

                rsi = float(latest["RSI"])

                atr = float(latest["ATR"])

                adx = float(latest["ADX"])

                volatility = float(latest["VOLATILITY"])

                ema20 = float(latest["EMA20"])

                ema50 = float(latest["EMA50"])

                relative_volume = round(volume / latest["VOL_MA20"], 2)

                # ======================================
                # NAN VALIDATION
                # ======================================

                if pd.isna(atr) or pd.isna(adx) or pd.isna(rsi):

                    continue

                # ======================================
                # BASIC FILTER
                # ======================================

                if price < 50:

                    continue

                if price > 5000:

                    continue

                if volume < 1_000_000:

                    continue

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

                if adx < min_adx:

                    continue

                # ======================================
                # VOLATILITY FILTER
                # ======================================

                if volatility > max_volatility:

                    continue

                # ======================================
                # RSI FILTER
                # ======================================

                if rsi < min_rsi or rsi > 85:

                    continue

                # ======================================
                # DAILY ANALYSIS
                # ======================================

                daily_analysis = analyze_daily_timeframe(df)

                if daily_analysis is None or daily_analysis["status"] == "WEAK":

                    continue

                # ======================================
                # WEEKLY ANALYSIS
                # ======================================

                weekly_df = df.copy()

                weekly_analysis = analyze_weekly_timeframe(weekly_df)

                if weekly_analysis is None or weekly_analysis["status"] == "WEAK":

                    continue

                # ======================================
                # RELATIVE STRENGTH
                # ======================================

                rs_analysis = calculate_relative_strength(df)

                if rs_analysis is None or rs_analysis["status"] == "WEAK":

                    continue

                # ======================================
                # MARKET FILTER
                # ======================================

                if market["status"] == "STRONG BEARISH":

                    if rs_analysis["status"] != "MARKET LEADER":

                        continue

                # ======================================
                # STRATEGY ENGINE
                # ======================================

                strategy_analysis = run_strategy(market["status"], latest, df)

                if strategy_analysis is None or strategy_analysis["status"] != "PASS":

                    continue

                # ======================================
                # BASE SCORE
                # ======================================

                score = calculate_score(latest, df)

                # ======================================
                # DAILY BONUS
                # ======================================

                score += int(daily_analysis["score"] * 0.2)

                # ======================================
                # WEEKLY BONUS
                # ======================================

                score += int(weekly_analysis["score"] * 0.15)

                # ======================================
                # RELATIVE STRENGTH BONUS
                # ======================================

                if rs_analysis["status"] == "MARKET LEADER":

                    score += 15

                elif rs_analysis["status"] == "STRONG":

                    score += 8

                # ======================================
                # TRADE PLAN
                # ======================================

                stop_loss = round(price - (2 * atr), 2)

                take_profit = round(price + (4 * atr), 2)

                risk = price - stop_loss

                if risk <= 0:

                    continue

                risk_reward = round((take_profit - price) / risk, 2)

                # ======================================
                # RISK REWARD BONUS
                # ======================================

                if risk_reward >= 2:

                    score += 5

                # ======================================
                # SCORE LIMIT
                # ======================================

                score = min(score, 100)

                # ======================================
                # MINIMUM SCORE
                # ======================================

                if score < 60:

                    continue

                # ======================================
                # AI CONFIDENCE
                # ======================================

                confidence_analysis = calculate_confidence(
                    market["status"],
                    weekly_analysis,
                    daily_analysis,
                    rs_analysis,
                    strategy_analysis,
                    latest,
                )

                # ======================================
                # META STRATEGY AI
                # ======================================

                meta_analysis = adjust_confidence(
                    confidence_analysis["confidence"],
                    strategy_analysis["strategy"],
                    market["status"],
                    learning_df,
                )

                final_confidence = meta_analysis["adjusted_confidence"]

                # ======================================
                # SAVE RESULT
                # ======================================

                results.append(
                    {
                        "Symbol": symbol,
                        "Price": round(price, 2),
                        "Volume": int(volume),
                        "Relative_Volume": (relative_volume),
                        "Value": int(value),
                        "RSI": round(rsi, 2),
                        "ATR": round(atr, 2),
                        "ADX": round(adx, 2),
                        "Volatility": round(volatility, 4),
                        "MA5": round(latest["MA5"], 2),
                        "MA20": round(latest["MA20"], 2),
                        "EMA20": round(ema20, 2),
                        "EMA50": round(ema50, 2),
                        "Score": score,
                        "Confidence": (final_confidence),
                        "Signal_Quality": (confidence_analysis["quality"]),
                        "Stop_Loss": stop_loss,
                        "Take_Profit": take_profit,
                        "Risk_Reward": risk_reward,
                        "Market": (market["status"]),
                        "Market_Regime": (market["status"]),
                        "Daily_Status": (daily_analysis["status"]),
                        "Daily_Score": (daily_analysis["score"]),
                        "Weekly_Status": (weekly_analysis["status"]),
                        "Weekly_Score": (weekly_analysis["score"]),
                        "RS_Ratio": (rs_analysis["rs_ratio"]),
                        "Relative_Performance": (rs_analysis["relative_performance"]),
                        "RS_Status": (rs_analysis["status"]),
                        "Strategy": (strategy_analysis["strategy"]),
                        "Strategy_Score": (strategy_analysis["score"]),
                        "Meta_Adjustment": (meta_analysis["adjustment"]),
                        "Meta_Reason": (meta_analysis["reason"]),
                        "AI_Mode": ("SELF_ADAPTIVE"),
                    }
                )

            except Exception as e:

                logger.error(f"{symbol} | {e}")

        # ======================================
        # RESULT DATAFRAME
        # ======================================

        result_df = pd.DataFrame(results)

        # ======================================
        # EMPTY RESULT
        # ======================================

        if result_df.empty:

            print("⚠️ No stocks passed screening")

            return (pd.DataFrame(), filtered_symbols)

        # ======================================
        # SORTING
        # ======================================

        result_df = result_df.sort_values(
            by=["Confidence", "Score", "RS_Ratio", "Relative_Volume"], ascending=False
        ).reset_index(drop=True)

        # ======================================
        # TOP RESULTS
        # ======================================

        result_df = result_df.head(50)

        print(f"✅ Total results: " f"{len(result_df)}")

        return (result_df, filtered_symbols)

    except Exception as e:

        print(f"❌ Screener Error: " f"{e}")

        return (pd.DataFrame(), filtered_symbols)
