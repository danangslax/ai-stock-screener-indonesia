from strategies.breakout_strategy import breakout_strategy

from strategies.defensive_strategy import defensive_strategy

from strategies.pullback_strategy import pullback_strategy

# ======================================
# STRATEGY ROUTER
# ======================================


def run_strategy(market_status, latest, df):

    try:

        # ======================================
        # STRONG BULL
        # ======================================

        if market_status == "STRONG_BULL":

            return breakout_strategy(latest, df)

        # ======================================
        # BULL
        # ======================================

        elif market_status == "BULL":

            breakout_result = breakout_strategy(latest, df)

            if breakout_result and breakout_result["status"] == "PASS":

                return breakout_result

            return pullback_strategy(latest, df)

        # ======================================
        # ACCUMULATION
        # ======================================

        elif market_status == "ACCUMULATION":

            return defensive_strategy(latest, df)

        # ======================================
        # SIDEWAYS
        # ======================================

        elif market_status == "SIDEWAYS":

            return defensive_strategy(latest, df)

        # ======================================
        # DISTRIBUTION
        # ======================================

        elif market_status == "DISTRIBUTION":

            return defensive_strategy(latest, df)

        # ======================================
        # PANIC
        # ======================================

        elif market_status == "PANIC":

            return defensive_strategy(latest, df)

        # ======================================
        # BEARISH
        # ======================================

        elif market_status == "BEARISH":

            return defensive_strategy(latest, df)

        # ======================================
        # RECOVERY
        # ======================================

        elif market_status == "RECOVERY":

            return breakout_strategy(latest, df)

        # ======================================
        # DEFAULT FALLBACK
        # ======================================

        return defensive_strategy(latest, df)

    except Exception as e:

        print(f"❌ Strategy router error: " f"{e}")

        return None
