from datetime import datetime

from ai.ai_parameters import (
    save_parameters,
    load_parameters,
)

from infrastructure.logger import logger

# ======================================
# AUTO TUNING ENGINE
# ======================================


def auto_tune_parameters(
    optimization_data,
    minimum_samples=20,
    blend_ratio=0.30,
):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not optimization_data:

            logger.warning("Auto tuning skipped | " "empty optimization data")

            return None

        # ======================================
        # SAMPLE VALIDATION
        # ======================================

        total_samples = optimization_data.get("total_samples", 0)

        if total_samples < minimum_samples:

            logger.warning(
                f"Auto tuning skipped | " f"insufficient samples: " f"{total_samples}"
            )

            return None

        # ======================================
        # LOAD CURRENT PARAMETERS
        # ======================================

        current_parameters = load_parameters()

        current_rsi = current_parameters.get("min_rsi", 50)

        current_adx = current_parameters.get("min_adx", 20)

        current_volatility = current_parameters.get("max_volatility", 0.10)

        # ======================================
        # OPTIMIZED PARAMETERS
        # ======================================

        optimal_rsi = optimization_data.get("optimal_rsi", current_rsi)

        optimal_adx = optimization_data.get("optimal_adx", current_adx)

        optimal_volatility = optimization_data.get(
            "optimal_volatility", current_volatility
        )

        # ======================================
        # BLENDED UPDATE
        # ======================================

        blended_rsi = current_rsi * (1 - blend_ratio) + optimal_rsi * blend_ratio

        blended_adx = current_adx * (1 - blend_ratio) + optimal_adx * blend_ratio

        blended_volatility = (
            current_volatility * (1 - blend_ratio) + optimal_volatility * blend_ratio
        )

        # ======================================
        # SAFETY LIMITS
        # ======================================

        blended_rsi = max(45, min(70, blended_rsi))

        blended_adx = max(15, min(40, blended_adx))

        blended_volatility = max(0.03, min(0.20, blended_volatility))

        # ======================================
        # PARAMETER DRIFT PROTECTION
        # ======================================

        max_rsi_change = 5

        max_adx_change = 5

        max_vol_change = 0.03

        # RSI
        if abs(blended_rsi - current_rsi) > max_rsi_change:

            blended_rsi = current_rsi + (
                max_rsi_change if blended_rsi > current_rsi else -max_rsi_change
            )

        # ADX
        if abs(blended_adx - current_adx) > max_adx_change:

            blended_adx = current_adx + (
                max_adx_change if blended_adx > current_adx else -max_adx_change
            )

        # VOLATILITY
        if abs(blended_volatility - current_volatility) > max_vol_change:

            blended_volatility = current_volatility + (
                max_vol_change
                if blended_volatility > current_volatility
                else -max_vol_change
            )

        # ======================================
        # FINAL PARAMETERS
        # ======================================

        parameters = {
            "min_rsi": round(blended_rsi, 2),
            "min_adx": round(blended_adx, 2),
            "max_volatility": round(blended_volatility, 4),
            "last_updated": str(datetime.now()),
            "total_samples": (total_samples),
            "blend_ratio": (blend_ratio),
        }

        # ======================================
        # SAVE PARAMETERS
        # ======================================

        save_parameters(parameters)

        logger.info("=================================")

        logger.info("AUTO TUNING COMPLETE")

        logger.info(f"Samples: " f"{total_samples}")

        logger.info(f"RSI: " f"{current_rsi} " f"→ " f"{parameters['min_rsi']}")

        logger.info(f"ADX: " f"{current_adx} " f"→ " f"{parameters['min_adx']}")

        logger.info(
            f"VOL: " f"{current_volatility} " f"→ " f"{parameters['max_volatility']}"
        )

        logger.info("=================================")

        return parameters

    except Exception as e:

        logger.error(f"Auto tuning " f"error: {e}")

        return None
