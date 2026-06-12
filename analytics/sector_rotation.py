import pandas as pd

from collections import defaultdict

from storage.data_loader import load_stock_data

from watchlist.sectors import SECTOR_MAP

# ======================================
# CALCULATE STOCK SCORE
# ======================================


def calculate_stock_score(df):

    try:

        latest = df.iloc[-1]

        score = 0

        close = float(latest["Close"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        volume = float(latest["Volume"])

        vol_ma20 = float(latest["VOL_MA20"])

        relative_volume = 0

        if vol_ma20 > 0:

            relative_volume = volume / vol_ma20

        # ======================================
        # TREND
        # ======================================

        if close > ema20:

            score += 20

        if ema20 > ema50:

            score += 20

        # ======================================
        # MOMENTUM
        # ======================================

        if rsi >= 55:

            score += 20

        # ======================================
        # TREND STRENGTH
        # ======================================

        if adx >= 20:

            score += 20

        # ======================================
        # VOLUME
        # ======================================

        if relative_volume >= 1.5:

            score += 20

        return score

    except:

        return 0


# ======================================
# ANALYZE SECTOR ROTATION
# ======================================


def analyze_sector_rotation(symbols):

    try:

        sector_data = defaultdict(list)

        # ======================================
        # LOOP STOCKS
        # ======================================

        for symbol in symbols:

            try:

                sector = SECTOR_MAP.get(
                    symbol,
                    "OTHER",
                )

                df = load_stock_data(symbol)

                if df.empty:

                    continue

                score = calculate_stock_score(df)

                sector_data[sector].append(
                    {
                        "symbol": symbol,
                        "score": score,
                    }
                )

            except:

                continue

        # ======================================
        # EMPTY
        # ======================================

        if not sector_data:

            return {}

        sector_scores = {}

        top_stocks_by_sector = {}

        sector_leaders = {}

        # ======================================
        # ANALYZE EACH SECTOR
        # ======================================

        for sector, stocks in sector_data.items():

            if not stocks:

                continue

            stocks = sorted(
                stocks,
                key=lambda x: x["score"],
                reverse=True,
            )

            avg_score = sum(s["score"] for s in stocks) / len(stocks)

            sector_scores[sector] = round(
                avg_score,
                2,
            )

            # ======================================
            # SECTOR LEADER
            # ======================================

            sector_leaders[sector] = stocks[0]

            # ======================================
            # TOP STOCKS
            # ======================================

            top_stocks_by_sector[sector] = stocks[:5]

        # ======================================
        # STRONGEST SECTOR
        # ======================================

        strongest_sector = max(
            sector_scores,
            key=sector_scores.get,
        )

        return {
            "strongest_sector": strongest_sector,
            "sector_scores": sector_scores,
            "sector_leaders": sector_leaders,
            "top_stocks_by_sector": top_stocks_by_sector,
        }

    except Exception as e:

        print(f"❌ Sector rotation error: {e}")

        return {}
