from datetime import datetime

import pandas as pd

# ======================================
# FORWARD TEST ENGINE
# ======================================


def create_forward_signal(signal_data):

    try:

        signal = {
            "date": str(datetime.now()),
            "symbol": signal_data["Symbol"],
            "price": signal_data["Price"],
            "confidence": signal_data["Confidence"],
            "strategy": signal_data["Strategy"],
            "market_regime": signal_data["Market"],
            "status": "ACTIVE",
            "forward_return": 0,
        }

        return signal

    except Exception as e:

        print(f"❌ Forward signal error: " f"{e}")

        return None


# ======================================
# ANALYZE FORWARD PERFORMANCE
# ======================================


def analyze_forward_testing(signals):

    try:

        if not signals:

            return {}

        df = pd.DataFrame(signals)

        # ======================================
        # TOTAL SIGNALS
        # ======================================

        total = len(df)

        # ======================================
        # WIN SIGNALS
        # ======================================

        wins = df[df["forward_return"] > 0]

        # ======================================
        # WINRATE
        # ======================================

        winrate = round((len(wins) / total) * 100, 2)

        # ======================================
        # AVG RETURN
        # ======================================

        avg_return = round(df["forward_return"].mean(), 2)

        # ======================================
        # HIGH CONFIDENCE
        # ======================================

        high_conf = df[df["confidence"] >= 80]

        high_conf_avg = 0

        if not high_conf.empty:

            high_conf_avg = round(high_conf["forward_return"].mean(), 2)

        return {
            "total_signals": total,
            "winrate": winrate,
            "average_return": (avg_return),
            "high_confidence_return": (high_conf_avg),
        }

    except Exception as e:

        print(f"❌ Forward testing error: " f"{e}")

        return {}
