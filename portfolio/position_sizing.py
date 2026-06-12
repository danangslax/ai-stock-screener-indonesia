# ======================================
# POSITION SIZING ENGINE
# ======================================


def calculate_position_size(capital, entry_price, stop_loss, risk_percent=1):

    try:

        # ======================================
        # RISK CAPITAL
        # ======================================

        risk_capital = capital * (risk_percent / 100)

        # ======================================
        # RISK PER SHARE
        # ======================================

        risk_per_share = entry_price - stop_loss

        # ======================================
        # VALIDATION
        # ======================================

        if risk_per_share <= 0:

            return None

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
        # FINAL RISK
        # ======================================

        max_loss = lots * 100 * risk_per_share

        return {
            "capital": capital,
            "risk_percent": risk_percent,
            "risk_capital": round(risk_capital, 2),
            "entry_price": round(entry_price, 2),
            "stop_loss": round(stop_loss, 2),
            "risk_per_share": round(risk_per_share, 2),
            "recommended_lots": lots,
            "position_value": round(position_value, 2),
            "max_loss": round(max_loss, 2),
        }

    except Exception as e:

        print(f"❌ Position sizing error: " f"{e}")

        return None
