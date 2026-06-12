import pandas as pd

from watchlist.sectors import SECTOR_MAP

from infrastructure.logger import logger

# ======================================
# DEFAULT RESULT
# ======================================

DEFAULT_RESULT = {
    "total_positions": 0,
    "total_exposure": 0,
    "cash_remaining": 0,
    "cash_ratio": 0,
    "sector_exposure": {},
    "largest_position": 0,
    "largest_position_pct": 0,
    "diversification_score": 0,
    "portfolio_heat": 0,
    "survivability_score": 0,
    "ai_portfolio_score": 0,
    "risk_status": "UNKNOWN",
}

# ======================================
# PORTFOLIO CONSTRUCTION ENGINE
# ======================================


def analyze_portfolio(
    trades,
    portfolio_balance=100_000_000,
    market_regime="SIDEWAYS",
):

    try:

        # ======================================
        # EMPTY VALIDATION
        # ======================================

        if not trades:

            return DEFAULT_RESULT.copy()

        # ======================================
        # DATAFRAME
        # ======================================

        df = pd.DataFrame(trades)

        if df.empty:

            return DEFAULT_RESULT.copy()

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [
            "symbol",
            "position_value",
            "status",
        ]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            logger.warning(f"Missing columns: " f"{missing}")

            return DEFAULT_RESULT.copy()

        # ======================================
        # OPEN POSITIONS ONLY
        # ======================================

        df = df[df["status"] == "OPEN"].copy()

        if df.empty:

            return DEFAULT_RESULT.copy()

        # ======================================
        # CLEAN DATA
        # ======================================

        df["position_value"] = pd.to_numeric(
            df["position_value"], errors="coerce"
        ).fillna(0)

        # ======================================
        # TOTAL EXPOSURE
        # ======================================

        total_exposure = round(df["position_value"].sum(), 2)

        # ======================================
        # CASH
        # ======================================

        cash_remaining = round(portfolio_balance - total_exposure, 2)

        cash_ratio = round((cash_remaining / portfolio_balance) * 100, 2)

        # ======================================
        # SECTOR MAPPING
        # ======================================

        df["sector"] = (
            df["symbol"]
            .astype(str)
            .str.replace(".JK", "", regex=False)
            .map(SECTOR_MAP)
            .fillna("OTHER")
        )

        # ======================================
        # SECTOR EXPOSURE
        # ======================================

        sector_group = df.groupby("sector")["position_value"].sum()

        sector_exposure = {}

        for sector, exposure in sector_group.items():

            exposure_pct = round((exposure / total_exposure) * 100, 2)

            sector_exposure[sector] = {
                "value": round(exposure, 2),
                "percentage": (exposure_pct),
            }

        # ======================================
        # POSITION CONCENTRATION
        # ======================================

        largest_position = round(df["position_value"].max(), 2)

        largest_position_pct = round((largest_position / total_exposure) * 100, 2)

        # ======================================
        # DIVERSIFICATION SCORE
        # ======================================

        unique_sectors = len(sector_exposure.keys())

        diversification_score = round(min(unique_sectors * 15, 100), 2)

        # ======================================
        # PORTFOLIO HEAT
        # ======================================

        portfolio_heat = round((total_exposure / portfolio_balance) * 100, 2)

        # ======================================
        # SURVIVABILITY SCORE
        # ======================================

        survivability_score = 100

        # Concentration penalty
        if largest_position_pct > 30:

            survivability_score -= 20

        # Sector penalty
        for sector_data in sector_exposure.values():

            if sector_data["percentage"] > 40:

                survivability_score -= 20

        # Heat penalty
        if portfolio_heat > 80:

            survivability_score -= 20

        survivability_score = max(survivability_score, 0)

        # ======================================
        # MARKET REGIME ADAPTATION
        # ======================================

        if market_regime == "PANIC":

            survivability_score -= 20

        elif market_regime == "BEARISH":

            survivability_score -= 10

        survivability_score = max(survivability_score, 0)

        # ======================================
        # AI PORTFOLIO SCORE
        # ======================================

        ai_portfolio_score = round(
            (diversification_score * 0.30)
            + (survivability_score * 0.40)
            + (max(0, 100 - portfolio_heat) * 0.30),
            2,
        )

        # ======================================
        # RISK STATUS
        # ======================================

        risk_status = "SAFE"

        if portfolio_heat > 90 or largest_position_pct > 40:

            risk_status = "DANGEROUS"

        elif portfolio_heat > 70 or largest_position_pct > 30:

            risk_status = "WARNING"

        # ======================================
        # RESULT
        # ======================================

        result = {
            "total_positions": (len(df)),
            "total_exposure": (total_exposure),
            "cash_remaining": (cash_remaining),
            "cash_ratio": (cash_ratio),
            "sector_exposure": (sector_exposure),
            "largest_position": (largest_position),
            "largest_position_pct": (largest_position_pct),
            "diversification_score": (diversification_score),
            "portfolio_heat": (portfolio_heat),
            "survivability_score": (survivability_score),
            "ai_portfolio_score": (ai_portfolio_score),
            "risk_status": (risk_status),
        }

        logger.info("Portfolio analysis complete")

        return result

    except Exception as e:

        logger.error(f"Portfolio engine " f"error: {e}")

        return DEFAULT_RESULT.copy()
