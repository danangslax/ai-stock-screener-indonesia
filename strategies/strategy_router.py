from infrastructure.logger import logger

from strategies.breakout_strategy import breakout_strategy

from strategies.defensive_strategy import defensive_strategy

from strategies.pullback_strategy import pullback_strategy

# ======================================
# STRATEGY ROUTER
# ======================================


def run_strategy(market_status, latest, df):

    try:

        logger.info(f"Routing strategy " f"for regime: " f"{market_status}")

        # ======================================
        # STRATEGY RESULTS
        # ======================================

        breakout_result = breakout_strategy(latest, df)

        defensive_result = defensive_strategy(latest, df)

        pullback_result = pullback_strategy(latest, df)

        # ======================================
        # CANDIDATES
        # ======================================

        candidates = []

        # ======================================
        # STRONG BULL
        # ======================================

        if market_status == "STRONG_BULL":

            if breakout_result:

                candidates.append(breakout_result)

            if pullback_result:

                candidates.append(pullback_result)

        # ======================================
        # BULL
        # ======================================

        elif market_status == "BULL":

            if breakout_result:

                candidates.append(breakout_result)

            if pullback_result:

                candidates.append(pullback_result)

        # ======================================
        # ACCUMULATION
        # ======================================

        elif market_status == "ACCUMULATION":

            if pullback_result:

                candidates.append(pullback_result)

            if defensive_result:

                candidates.append(defensive_result)

        # ======================================
        # SIDEWAYS
        # ======================================

        elif market_status == "SIDEWAYS":

            if defensive_result:

                candidates.append(defensive_result)

        # ======================================
        # DISTRIBUTION
        # ======================================

        elif market_status == "DISTRIBUTION":

            if defensive_result:

                candidates.append(defensive_result)

        # ======================================
        # PANIC
        # ======================================

        elif market_status == "PANIC":

            if defensive_result:

                candidates.append(defensive_result)

        # ======================================
        # BEARISH
        # ======================================

        elif market_status == "BEARISH":

            if defensive_result:

                candidates.append(defensive_result)

        # ======================================
        # RECOVERY
        # ======================================

        elif market_status == "RECOVERY":

            if pullback_result:

                candidates.append(pullback_result)

            if breakout_result:

                candidates.append(breakout_result)

        # ======================================
        # UNKNOWN
        # ======================================

        else:

            if defensive_result:

                candidates.append(defensive_result)

        # ======================================
        # VALIDATION
        # ======================================

        if not candidates:

            return None

        # ======================================
        # SORT BY SCORE
        # ======================================

        candidates = sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)

        # ======================================
        # BEST STRATEGY
        # ======================================

        best_strategy = candidates[0]

        # ======================================
        # ADD ROUTING INFO
        # ======================================

        best_strategy["market_regime"] = market_status

        best_strategy["candidate_count"] = len(candidates)

        logger.info(
            f"Selected strategy: "
            f"{best_strategy['strategy']} "
            f"| Score="
            f"{best_strategy['score']}"
        )

        return best_strategy

    except Exception as e:

        logger.error(f"Strategy router " f"error: {e}")

        return None
