from pathlib import Path

import pandas as pd

from storage.data_loader import (
    load_stock_data,
)

from screener.scoring import (
    calculate_score,
)

from market.market import (
    get_market_status,
)

from screener.daily_timeframe import (
    analyze_daily_timeframe,
)

from screener.relative_strength import (
    calculate_relative_strength,
)

from screener.universe_filter import (
    filter_universe,
)

from strategies.strategy_router import (
    run_strategy,
)

from screener.weekly_timeframe import (
    analyze_weekly_timeframe,
)

from screener.confidence import (
    calculate_confidence,
)

from ai.meta_strategy import (
    adjust_confidence,
)

from trading.trade_journal import (
    load_journal,
)

from ai.learning_engine import (
    analyze_learning_data,
)

from ai.ai_parameters import (
    load_parameters,
)

from infrastructure.logger import (
    logger,
)

# ======================================
# BASE DIRECTORY
# ======================================

BASE_DIR = Path(__file__).resolve().parents[1]

# ======================================
# WATCHLIST PATH
# ======================================

WATCHLIST_PATH = BASE_DIR / "watchlist" / "idx_stocks.txt"

# ======================================
# LOAD WATCHLIST
# ======================================

with open(
    WATCHLIST_PATH,
    "r",
    encoding="utf-8",
) as f:
    IDX_STOCKS = [line.strip() for line in f if line.strip()]

logger.info(f"Total saham: " f"{len(IDX_STOCKS)}")

# ======================================
# AI SCREENER ENGINE
# ======================================


def run_screener():

    filtered_symbols = []

    try:

        logger.info("Starting AI Screener")

        # ======================================
        # MARKET STATUS
        # ======================================

        market = get_market_status()

        market_status = market.get("status", "UNKNOWN")

        logger.info(f"Market Status: " f"{market_status}")

        # ======================================
        # LOAD AI PARAMETERS
        # ======================================

        ai_parameters = load_parameters()

        min_rsi = ai_parameters.get("min_rsi", 50)

        min_adx = ai_parameters.get("min_adx", 20)

        max_volatility = ai_parameters.get("max_volatility", 0.10)

        logger.info(
            f"AI Parameters | "
            f"RSI={min_rsi} | "
            f"ADX={min_adx} | "
            f"VOL={max_volatility}"
        )

        # ======================================
        # LOAD LEARNING DATA
        # ======================================

        journal_data = load_journal()

        learning_df = analyze_learning_data(journal_data)

        # ======================================
        # FAST UNIVERSE FILTER
        # ======================================

        filtered_symbols = filter_universe(IDX_STOCKS)

        total = len(filtered_symbols)

        logger.info(f"Filtered Universe: " f"{total}")

        # ======================================
        # EMPTY FILTER
        # ======================================

        if total == 0:

            logger.warning("Universe filter empty")

            return (pd.DataFrame(), [])

        # ======================================
        # BENCHMARK CACHE
        # ======================================

        benchmark_df = load_stock_data(
            "^JKSE",
            period="6mo",
            interval="1d",
            use_cache=True,
        )

        # ======================================
        # RESULT CONTAINER
        # ======================================

        results = []

        # ======================================
        # FILTER STATISTICS
        # ======================================

        failed_data = 0
        failed_basic = 0
        failed_trend = 0
        failed_rsi = 0
        failed_adx = 0
        failed_volatility = 0
        failed_daily = 0
        failed_weekly = 0
        failed_rs = 0
        failed_strategy = 0

        # ======================================
        # LOOP STOCKS
        # ======================================

        for i, symbol in enumerate(filtered_symbols):

            logger.info(f"Scanning " f"{i+1}/{total}: " f"{symbol}")

            try:

                # ======================================
                # LOAD DATA
                # ======================================

                df = load_stock_data(
                    symbol,
                    period="6mo",
                    interval="1d",
                    use_cache=True,
                )

                # ======================================
                # VALIDATION
                # ======================================

                if df.empty:

                    failed_data += 1

                    continue

                if len(df) < 60:

                    failed_data += 1

                    continue

                latest = df.iloc[-1]

                # ======================================
                # REQUIRED COLUMNS
                # ======================================

                required_columns = [
                    "Close",
                    "Volume",
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

                    logger.warning(
                        f"{symbol} " f"Missing columns: " f"{missing_columns}"
                    )

                    failed_data += 1

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

                vol_ma20 = float(latest["VOL_MA20"])

                # ======================================
                # NAN VALIDATION
                # ======================================

                metrics = [
                    price,
                    volume,
                    value,
                    rsi,
                    atr,
                    adx,
                    volatility,
                    ema20,
                    ema50,
                    vol_ma20,
                ]

                if any(pd.isna(v) for v in metrics):

                    failed_data += 1

                    continue

                # ======================================
                # RELATIVE VOLUME
                # ======================================

                if vol_ma20 <= 0:

                    failed_data += 1

                    continue

                relative_volume = round(
                    volume / vol_ma20,
                    2,
                )

                # ======================================
                # BASIC FILTER
                # ======================================

                if price < 50:

                    failed_basic += 1

                    continue

                if price > 5000:

                    failed_basic += 1

                    continue

                if volume < 1_000_000:

                    failed_basic += 1

                    continue

                if value < 15_000_000_000:

                    failed_basic += 1

                    continue

                # ======================================
                # TREND FILTER
                # ======================================

                if ema20 < ema50:

                    failed_trend += 1

                    continue

                # ======================================
                # ADX FILTER
                # ======================================

                if adx < min_adx:

                    failed_adx += 1

                    continue

                # ======================================
                # VOLATILITY FILTER
                # ======================================

                if volatility > max_volatility:

                    failed_volatility += 1

                    continue

                # ======================================
                # RSI FILTER
                # ======================================

                if rsi < min_rsi:

                    failed_rsi += 1

                    continue

                if rsi > 85:

                    failed_rsi += 1

                    continue

                # ======================================
                # DAILY ANALYSIS
                # ======================================

                daily_analysis = analyze_daily_timeframe(df)

                if daily_analysis is None or daily_analysis["status"] == "WEAK":

                    failed_daily += 1

                    continue

                # ======================================
                # WEEKLY ANALYSIS
                # ======================================

                weekly_analysis = analyze_weekly_timeframe(df)

                if weekly_analysis is None or weekly_analysis["status"] == "WEAK":

                    failed_weekly += 1

                    continue

                # ======================================
                # RELATIVE STRENGTH
                # ======================================

                rs_analysis = calculate_relative_strength(
                    stock_df=df,
                    benchmark_df=benchmark_df,
                )

                if rs_analysis is None or rs_analysis["status"] == "WEAK":

                    failed_rs += 1

                    continue

                # ======================================
                # BEARISH MARKET FILTER
                # ======================================

                if market_status in [
                    "BEARISH",
                    "PANIC",
                ]:

                    if rs_analysis["status"] != "MARKET LEADER":

                        failed_rs += 1

                        continue

                # ======================================
                # STRATEGY ENGINE
                # ======================================

                strategy_analysis = run_strategy(
                    market_status,
                    latest,
                    df,
                )

                if strategy_analysis is None or strategy_analysis["status"] != "PASS":

                    failed_strategy += 1

                    continue

                # ======================================
                # BASE SCORE
                # ======================================

                score_analysis = calculate_score(latest)

                score = score_analysis["score"]

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

                stop_loss = round(
                    price - (2 * atr),
                    2,
                )

                take_profit = round(
                    price + (4 * atr),
                    2,
                )

                risk = price - stop_loss

                if risk <= 0:

                    continue

                risk_reward = round(
                    (take_profit - price) / risk,
                    2,
                )

                # ======================================
                # RISK REWARD BONUS
                # ======================================

                if risk_reward >= 2:

                    score += 5

                # ======================================
                # FINAL SCORE LIMIT
                # ======================================

                score = min(
                    score,
                    100,
                )

                # ======================================
                # MINIMUM SCORE
                # ======================================

                if score < 60:

                    continue

                # ======================================
                # AI CONFIDENCE
                # ======================================

                confidence_analysis = calculate_confidence(
                    market_status,
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
                    market_status,
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
                        "Stop_Loss": (stop_loss),
                        "Take_Profit": (take_profit),
                        "Risk_Reward": (risk_reward),
                        "Market": (market_status),
                        "Market_Regime": (market_status),
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

            logger.warning("No stocks passed screening")

            return (
                pd.DataFrame(),
                filtered_symbols,
            )

        # ======================================
        # SORT RESULTS
        # ======================================

        result_df = result_df.sort_values(
            by=[
                "Confidence",
                "Score",
                "RS_Ratio",
                "Relative_Volume",
            ],
            ascending=False,
        ).reset_index(drop=True)

        # ======================================
        # TOP RESULTS
        # ======================================

        result_df = result_df.head(50)

        # ======================================
        # SUMMARY
        # ======================================

        logger.info("=================================")

        logger.info(f"Final Results: " f"{len(result_df)}")

        logger.info(f"Failed Data: " f"{failed_data}")

        logger.info(f"Failed Basic: " f"{failed_basic}")

        logger.info(f"Failed Trend: " f"{failed_trend}")

        logger.info(f"Failed RSI: " f"{failed_rsi}")

        logger.info(f"Failed ADX: " f"{failed_adx}")

        logger.info(f"Failed Volatility: " f"{failed_volatility}")

        logger.info(f"Failed Daily: " f"{failed_daily}")

        logger.info(f"Failed Weekly: " f"{failed_weekly}")

        logger.info(f"Failed RS: " f"{failed_rs}")

        logger.info(f"Failed Strategy: " f"{failed_strategy}")

        logger.info("=================================")

        return (
            result_df,
            filtered_symbols,
        )

    except Exception as e:

        logger.error(f"Screener Error: {e}")

        return (
            pd.DataFrame(),
            filtered_symbols,
        )
