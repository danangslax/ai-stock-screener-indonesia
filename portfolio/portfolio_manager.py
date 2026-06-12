import pandas as pd

# ======================================
# PORTFOLIO CONSTRUCTION ENGINE
# ======================================


def analyze_portfolio(trades):

    try:

        if not trades:

            return {
                "total_positions": 0,
                "total_exposure": 0,
                "sector_exposure": {},
                "risk_status": "SAFE",
            }

        df = pd.DataFrame(trades)

        # ======================================
        # VALIDATION
        # ======================================

        required_columns = ["symbol", "position_value"]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            return {
                "total_positions": 0,
                "total_exposure": 0,
                "sector_exposure": {},
                "risk_status": "UNKNOWN",
            }

        # ======================================
        # TOTAL EXPOSURE
        # ======================================

        total_exposure = float(df["position_value"].sum())

        # ======================================
        # MOCK SECTOR MAP
        # ======================================

        sector_map = {
            "BBCA": "BANKING",
            "BBRI": "BANKING",
            "BMRI": "BANKING",
            "ANTM": "MINING",
            "MDKA": "MINING",
            "BRMS": "MINING",
            "TINS": "MINING",
            "MEDC": "ENERGY",
            "PGAS": "ENERGY",
        }

        # ======================================
        # SECTOR COLUMN
        # ======================================

        df["sector"] = (
            df["symbol"]
            .str.replace(".JK", "", regex=False)
            .map(sector_map)
            .fillna("OTHER")
        )

        # ======================================
        # SECTOR EXPOSURE
        # ======================================

        sector_exposure = df.groupby("sector")["position_value"].sum().to_dict()

        # ======================================
        # RISK STATUS
        # ======================================

        risk_status = "SAFE"

        for sector, exposure in sector_exposure.items():

            exposure_percent = exposure / total_exposure

            if exposure_percent >= 0.4:

                risk_status = "HIGH_SECTOR_CONCENTRATION"

        return {
            "total_positions": len(df),
            "total_exposure": round(total_exposure, 2),
            "sector_exposure": sector_exposure,
            "risk_status": risk_status,
        }

    except Exception as e:

        print(f"❌ Portfolio engine error: " f"{e}")

        return {
            "total_positions": 0,
            "total_exposure": 0,
            "sector_exposure": {},
            "risk_status": "ERROR",
        }
