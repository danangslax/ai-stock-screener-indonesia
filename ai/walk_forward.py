import pandas as pd

from infrastructure.logger import logger

# ======================================
# WALK FORWARD OPTIMIZATION ENGINE
# ======================================


def optimize_parameters(screener_df, minimum_samples=20):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if screener_df.empty:

            logger.warning("Walk forward received " "empty dataframe")

            return {}

        # ======================================
        # DATAFRAME
        # ======================================

        df = screener_df.copy()

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required = [
            "RSI",
            "ADX",
            "Volatility",
            "Confidence",
        ]

        missing = [col for col in required if col not in df.columns]

        if missing:

            logger.warning(f"Walk forward " f"missing columns: " f"{missing}")

            return {}

        # ======================================
        # CLEAN NUMERIC
        # ======================================

        numeric_columns = [
            "RSI",
            "ADX",
            "Volatility",
            "Confidence",
        ]

        for col in numeric_columns:

            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        # ======================================
        # SAMPLE SIZE
        # ======================================

        if len(df) < minimum_samples:

            logger.warning(f"Walk forward " f"insufficient samples: " f"{len(df)}")

            return {}

        # ======================================
        # HIGH CONFIDENCE FILTER
        # ======================================

        strong_df = df[df["Confidence"] >= 80]

        # ======================================
        # VALIDATION
        # ======================================

        if len(strong_df) < minimum_samples:

            logger.warning("Insufficient high " "confidence samples")

            return {}

        # ======================================
        # OUTLIER FILTER
        # ======================================

        strong_df = strong_df[strong_df["RSI"].between(40, 90)]

        strong_df = strong_df[strong_df["ADX"].between(10, 60)]

        strong_df = strong_df[strong_df["Volatility"].between(0.01, 0.30)]

        if strong_df.empty:

            return {}

        # ======================================
        # WEIGHTED CONFIDENCE
        # ======================================

        weights = strong_df["Confidence"] / 100

        # ======================================
        # OPTIMAL PARAMETERS
        # ======================================

        optimal_rsi = round((strong_df["RSI"] * weights).sum() / weights.sum(), 2)

        optimal_adx = round((strong_df["ADX"] * weights).sum() / weights.sum(), 2)

        optimal_volatility = round(
            (strong_df["Volatility"] * weights).sum() / weights.sum(), 4
        )

        # ======================================
        # ROBUSTNESS SCORE
        # ======================================

        confidence_mean = round(strong_df["Confidence"].mean(), 2)

        robustness_score = round((confidence_mean * 0.6) + (len(strong_df) * 0.4), 2)

        robustness_score = min(robustness_score, 100)

        # ======================================
        # ROBUSTNESS STATUS
        # ======================================

        if robustness_score >= 80:

            robustness = "ROBUST"

        elif robustness_score >= 60:

            robustness = "STABLE"

        else:

            robustness = "WEAK"

        # ======================================
        # AI INSIGHT
        # ======================================

        insight = f"""
Walk Forward Optimization

Optimal RSI:
{optimal_rsi}

Optimal ADX:
{optimal_adx}

Optimal Volatility:
{optimal_volatility}

Samples:
{len(strong_df)}

Robustness:
{robustness}
"""

        # ======================================
        # RESULT
        # ======================================

        result = {
            "optimal_rsi": (optimal_rsi),
            "optimal_adx": (optimal_adx),
            "optimal_volatility": (optimal_volatility),
            "total_samples": (len(strong_df)),
            "robustness_score": (robustness_score),
            "robustness": (robustness),
            "average_confidence": (confidence_mean),
            "insight": (insight),
        }

        logger.info(
            f"Walk forward complete | "
            f"Samples={len(strong_df)} | "
            f"Robustness={robustness}"
        )

        return result

    except Exception as e:

        logger.error(f"Walk forward " f"optimization " f"error: {e}")

        return {}
