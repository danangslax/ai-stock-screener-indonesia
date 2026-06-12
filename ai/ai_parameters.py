import json

from pathlib import Path

# ======================================
# PARAMETER FILE
# ======================================

PARAMETER_PATH = Path("data") / "ai_parameters.json"

# ======================================
# DEFAULT PARAMETERS
# ======================================

DEFAULT_PARAMETERS = {"min_rsi": 50, "min_adx": 20, "max_volatility": 0.15}

# ======================================
# LOAD PARAMETERS
# ======================================


def load_parameters():

    try:

        if not PARAMETER_PATH.exists():

            save_parameters(DEFAULT_PARAMETERS)

            return DEFAULT_PARAMETERS

        with open(PARAMETER_PATH, "r", encoding="utf-8") as f:

            return json.load(f)

    except Exception as e:

        print(f"❌ Load parameter error: " f"{e}")

        return DEFAULT_PARAMETERS


# ======================================
# SAVE PARAMETERS
# ======================================


def save_parameters(parameters):

    try:

        PARAMETER_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(PARAMETER_PATH, "w", encoding="utf-8") as f:

            json.dump(parameters, f, indent=4)

        print("✅ AI parameters updated")

    except Exception as e:

        print(f"❌ Save parameter error: " f"{e}")
