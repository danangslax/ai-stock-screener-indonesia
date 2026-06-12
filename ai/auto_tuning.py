from ai.ai_parameters import save_parameters

# ======================================
# AUTO TUNING ENGINE
# ======================================


def auto_tune_parameters(optimization_data):

    try:

        if not optimization_data:

            return None

        optimal_rsi = optimization_data.get("optimal_rsi", 50)

        optimal_adx = optimization_data.get("optimal_adx", 20)

        optimal_volatility = optimization_data.get("optimal_volatility", 0.15)

        # ======================================
        # SAFETY LIMITS
        # ======================================

        optimal_rsi = max(45, min(70, optimal_rsi))

        optimal_adx = max(15, min(40, optimal_adx))

        optimal_volatility = max(0.03, min(0.20, optimal_volatility))

        # ======================================
        # SAVE NEW PARAMETERS
        # ======================================

        parameters = {
            "min_rsi": round(optimal_rsi, 2),
            "min_adx": round(optimal_adx, 2),
            "max_volatility": round(optimal_volatility, 4),
        }

        save_parameters(parameters)

        return parameters

    except Exception as e:

        print(f"❌ Auto tuning error: " f"{e}")

        return None
