import json

from datetime import datetime

from pathlib import Path

from infrastructure.logger import logger

# ======================================
# PARAMETER FILE
# ======================================

PARAMETER_PATH = Path("data") / "configs" / "ai_parameters.json"

# ======================================
# DEFAULT PARAMETERS
# ======================================

DEFAULT_PARAMETERS = {
    "min_rsi": 50,
    "min_adx": 20,
    "max_volatility": 0.15,
    "last_updated": None,
    "version": "1.0",
    "source": "default",
}

# ======================================
# VALIDATE PARAMETERS
# ======================================


def validate_parameters(parameters):

    try:

        # ======================================
        # REQUIRED KEYS
        # ======================================

        required_keys = [
            "min_rsi",
            "min_adx",
            "max_volatility",
        ]

        # ======================================
        # MISSING KEYS
        # ======================================

        for key in required_keys:

            if key not in parameters:

                logger.warning(f"Missing parameter: " f"{key}")

                parameters[key] = DEFAULT_PARAMETERS[key]

        # ======================================
        # TYPE CONVERSION
        # ======================================

        parameters["min_rsi"] = float(parameters["min_rsi"])

        parameters["min_adx"] = float(parameters["min_adx"])

        parameters["max_volatility"] = float(parameters["max_volatility"])

        # ======================================
        # SANITY CHECK
        # ======================================

        parameters["min_rsi"] = max(40, min(80, parameters["min_rsi"]))

        parameters["min_adx"] = max(10, min(50, parameters["min_adx"]))

        parameters["max_volatility"] = max(
            0.01, min(0.30, parameters["max_volatility"])
        )

        return parameters

    except Exception as e:

        logger.error(f"Parameter validation " f"error: {e}")

        return DEFAULT_PARAMETERS.copy()


# ======================================
# LOAD PARAMETERS
# ======================================


def load_parameters():

    try:

        # ======================================
        # FILE NOT EXISTS
        # ======================================

        if not PARAMETER_PATH.exists():

            logger.warning("AI parameter file missing")

            save_parameters(DEFAULT_PARAMETERS)

            return DEFAULT_PARAMETERS.copy()

        # ======================================
        # LOAD JSON
        # ======================================

        with open(PARAMETER_PATH, "r", encoding="utf-8") as f:

            parameters = json.load(f)

        # ======================================
        # VALIDATE
        # ======================================

        validated = validate_parameters(parameters)

        logger.info("AI parameters loaded")

        return validated

    except Exception as e:

        logger.error(f"Load parameter " f"error: {e}")

        logger.warning("Using default parameters")

        return DEFAULT_PARAMETERS.copy()


# ======================================
# SAVE PARAMETERS
# ======================================


def save_parameters(parameters):

    try:

        # ======================================
        # CREATE DIRECTORY
        # ======================================

        PARAMETER_PATH.parent.mkdir(parents=True, exist_ok=True)

        # ======================================
        # VALIDATE
        # ======================================

        validated = validate_parameters(parameters)

        # ======================================
        # METADATA
        # ======================================

        validated["last_updated"] = datetime.now().isoformat()

        # ======================================
        # TEMP FILE
        # ======================================

        temp_path = PARAMETER_PATH.with_suffix(".tmp")

        # ======================================
        # ATOMIC WRITE
        # ======================================

        with open(temp_path, "w", encoding="utf-8") as f:

            json.dump(validated, f, indent=4)

        # ======================================
        # REPLACE FILE
        # ======================================

        temp_path.replace(PARAMETER_PATH)

        logger.info("AI parameters updated")

        return True

    except Exception as e:

        logger.error(f"Save parameter " f"error: {e}")

        return False
