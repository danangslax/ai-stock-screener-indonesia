from infrastructure.logger import logger

# ======================================
# POSITION SIZING ENGINE
# ======================================


def calculate_position_size(
    capital,
    entry_price,
    stop_loss,
    risk_percent=1,
    market_regime="SIDEWAYS",
    current_portfolio_heat=0,
    average_volume=None,
    atr=None,
):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if capital <= 0:

            raise ValueError("Invalid capital")

        if entry_price <= 0:

            raise ValueError("Invalid entry price")

        if stop_loss <= 0:

            raise ValueError("Invalid stop loss")

        # ======================================
        # MARKET REGIME ADJUSTMENT
        # ======================================

        adjusted_risk = risk_percent

        if market_regime == "PANIC":

            adjusted_risk *= 0.3

        elif market_regime == "BEARISH":

            adjusted_risk *= 0.5

        elif market_regime == "SIDEWAYS":

            adjusted_risk *= 0.8

        elif market_regime in [
            "BULL",
            "STRONG_BULL",
            "RECOVERY",
        ]:

            adjusted_risk *= 1.0

        # ======================================
        # PORTFOLIO HEAT PROTECTION
        # ======================================

        if current_portfolio_heat >= 80:

            adjusted_risk *= 0.5

        elif current_portfolio_heat >= 60:

            adjusted_risk *= 0.7

        # ======================================
        # RISK CAPITAL
        # ======================================

        risk_capital = capital * (adjusted_risk / 100)

        # ======================================
        # RISK PER SHARE
        # ======================================

        risk_per_share = entry_price - stop_loss

        # ======================================
        # VALIDATION
        # ======================================

        if risk_per_share <= 0:

            logger.warning("Invalid risk per share")

            return None

        # ======================================
        # ATR ADJUSTMENT
        # ======================================

        if atr is not None:

            atr_ratio = atr / entry_price

            # High volatility reduction
            if atr_ratio > 0.08:

                risk_capital *= 0.7

            elif atr_ratio > 0.05:

                risk_capital *= 0.85

        # ======================================
        # TOTAL SHARES
        # ======================================

        shares = int(risk_capital / risk_per_share)

        # ======================================
        # LOT SIZE
        # ======================================

        lots = int(shares / 100)

        # ======================================
        # POSITION VALUE
        # ======================================

        position_value = lots * 100 * entry_price

        # ======================================
        # MAX EXPOSURE LIMIT
        # ======================================

        max_position_value = capital * 0.20

        if position_value > max_position_value:

            position_value = max_position_value

            lots = int(position_value / (entry_price * 100))

        # ======================================
        # LIQUIDITY PROTECTION
        # ======================================

        liquidity_warning = False

        if average_volume is not None:

            estimated_trade_size = lots * 100

            if estimated_trade_size > (average_volume * 0.02):

                liquidity_warning = True

                lots = int(lots * 0.5)

        # ======================================
        # RECALCULATE FINAL
        # ======================================

        position_value = round(lots * 100 * entry_price, 2)

        max_loss = round(lots * 100 * risk_per_share, 2)

        # ======================================
        # SLIPPAGE BUFFER
        # ======================================

        slippage_buffer = round(position_value * 0.002, 2)

        estimated_real_risk = round(max_loss + slippage_buffer, 2)

        # ======================================
        # RISK CLASSIFICATION
        # ======================================

        risk_level = "LOW"

        real_risk_pct = (estimated_real_risk / capital) * 100

        if real_risk_pct >= 2:

            risk_level = "HIGH"

        elif real_risk_pct >= 1:

            risk_level = "MEDIUM"

        # ======================================
        # SURVIVABILITY SCORE
        # ======================================

        survivability_score = 100

        # Heat penalty
        survivability_score -= current_portfolio_heat * 0.3

        # Risk penalty
        survivability_score -= real_risk_pct * 10

        survivability_score = max(0, round(survivability_score, 2))

        logger.info("Position sizing calculated")

        # ======================================
        # RETURN RESULT
        # ======================================

        return {
            "capital": (capital),
            "risk_percent": (round(adjusted_risk, 2)),
            "risk_capital": (round(risk_capital, 2)),
            "entry_price": (round(entry_price, 2)),
            "stop_loss": (round(stop_loss, 2)),
            "risk_per_share": (round(risk_per_share, 2)),
            "recommended_lots": (lots),
            "position_value": (position_value),
            "max_loss": (max_loss),
            "slippage_buffer": (slippage_buffer),
            "estimated_real_risk": (estimated_real_risk),
            "risk_level": (risk_level),
            "liquidity_warning": (liquidity_warning),
            "survivability_score": (survivability_score),
        }

    except Exception as e:

        logger.error(f"Position sizing " f"error: {e}")

        return None
