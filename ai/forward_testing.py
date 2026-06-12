from datetime import datetime

import pandas as pd

from infrastructure.logger import logger

# ======================================
# FORWARD TEST ENGINE
# ======================================


def create_forward_signal(signal_data):

    try:

        # ======================================
        # REQUIRED FIELDS
        # ======================================

        required_fields = [
            "Symbol",
            "Price",
            "Confidence",
            "Strategy",
            "Market",
        ]

        missing = [field for field in required_fields if field not in signal_data]

        if missing:

            logger.warning(f"Forward signal " f"missing fields: " f"{missing}")

            return None

        # ======================================
        # TIMESTAMP
        # ======================================

        now = datetime.now()

        # ======================================
        # SIGNAL ID
        # ======================================

        signal_id = f"{signal_data['Symbol']}_" f"{now.strftime('%Y%m%d_%H%M%S')}"

        # ======================================
        # SIGNAL OBJECT
        # ======================================

        signal = {
            "signal_id": (signal_id),
            "created_at": (now.isoformat()),
            "symbol": (signal_data["Symbol"]),
            "price": float(signal_data["Price"]),
            "confidence": int(signal_data["Confidence"]),
            "strategy": (signal_data["Strategy"]),
            "market_regime": (signal_data["Market"]),
            "status": "ACTIVE",
            "forward_return": 0,
            "holding_days": 0,
            "max_gain": 0,
            "max_loss": 0,
        }

        logger.info(f"Forward signal created | " f"{signal_id}")

        return signal

    except Exception as e:

        logger.error(f"Forward signal " f"error: {e}")

        return None


# ======================================
# ANALYZE FORWARD PERFORMANCE
# ======================================


def analyze_forward_testing(signals):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not signals:

            logger.warning("Forward testing " "received empty signals")

            return {}

        # ======================================
        # DATAFRAME
        # ======================================

        df = pd.DataFrame(signals)

        if df.empty:

            return {}

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [
            "forward_return",
            "confidence",
            "status",
        ]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            logger.warning(f"Forward testing " f"missing columns: " f"{missing}")

            return {}

        # ======================================
        # CLEAN DATA
        # ======================================

        df["forward_return"] = pd.to_numeric(df["forward_return"], errors="coerce")

        df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")

        df = df.dropna()

        if df.empty:

            return {}

        # ======================================
        # TOTAL SIGNALS
        # ======================================

        total = len(df)

        # ======================================
        # WIN SIGNALS
        # ======================================

        wins = df[df["forward_return"] > 0]

        losses = df[df["forward_return"] <= 0]

        # ======================================
        # WINRATE
        # ======================================

        winrate = round((len(wins) / total) * 100, 2)

        # ======================================
        # RETURNS
        # ======================================

        avg_return = round(df["forward_return"].mean(), 2)

        avg_win = 0

        avg_loss = 0

        if not wins.empty:

            avg_win = round(wins["forward_return"].mean(), 2)

        if not losses.empty:

            avg_loss = round(losses["forward_return"].mean(), 2)

        # ======================================
        # EXPECTANCY
        # ======================================

        expectancy = round(
            ((winrate / 100) * avg_win) + ((1 - (winrate / 100)) * avg_loss), 2
        )

        # ======================================
        # HIGH CONFIDENCE
        # ======================================

        high_conf = df[df["confidence"] >= 80]

        high_conf_avg = 0

        high_conf_winrate = 0

        if not high_conf.empty:

            high_conf_avg = round(high_conf["forward_return"].mean(), 2)

            high_conf_winrate = round(
                (len(high_conf[high_conf["forward_return"] > 0]) / len(high_conf))
                * 100,
                2,
            )

        # ======================================
        # MAX GAIN / LOSS
        # ======================================

        max_gain = round(df["forward_return"].max(), 2)

        max_loss = round(df["forward_return"].min(), 2)

        # ======================================
        # PROFIT FACTOR
        # ======================================

        gross_profit = wins["forward_return"].sum()

        gross_loss = abs(losses["forward_return"].sum())

        profit_factor = 0

        if gross_loss > 0:

            profit_factor = round(gross_profit / gross_loss, 2)

        # ======================================
        # RESULT
        # ======================================

        result = {
            "total_signals": (total),
            "winrate": (winrate),
            "average_return": (avg_return),
            "average_win": (avg_win),
            "average_loss": (avg_loss),
            "expectancy": (expectancy),
            "profit_factor": (profit_factor),
            "high_confidence_return": (high_conf_avg),
            "high_confidence_winrate": (high_conf_winrate),
            "max_gain": (max_gain),
            "max_loss": (max_loss),
        }

        logger.info(
            f"Forward testing analyzed | "
            f"Signals={total} | "
            f"Winrate={winrate}% | "
            f"PF={profit_factor}"
        )

        return result

    except Exception as e:

        logger.error(f"Forward testing " f"error: {e}")

        return {}
