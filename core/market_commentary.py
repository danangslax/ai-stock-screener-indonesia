import pandas as pd

from core.market import (
    get_market_status
)

from core.market_breadth import (
    analyze_market_breadth
)

from core.sector_strength import (
    analyze_sector_strength
)

# ======================================
# GENERATE MARKET COMMENTARY
# ======================================

def generate_market_commentary(

    symbols,

    screener_df=None
):

    try:

        # ======================================
        # MARKET STATUS
        # ======================================

        market = get_market_status()

        # ======================================
        # MARKET BREADTH
        # ======================================

        breadth = (
            analyze_market_breadth(
                symbols[:150]
            )
        )

        # ======================================
        # SECTOR STRENGTH
        # ======================================

        sector_df = (
            analyze_sector_strength()
        )

        # ======================================
        # TOP SECTOR
        # ======================================

        strongest_sector = "N/A"

        sector_leader = "N/A"

        if not sector_df.empty:

            top_sector = sector_df.iloc[0]

            strongest_sector = (
                top_sector["Sector"]
            )

            sector_leader = (
                top_sector["Leader"]
            )

        # ======================================
        # TOP PICKS
        # ======================================

        top_picks = []

        if (

            screener_df is not None

            and

            not screener_df.empty
        ):

            top_picks = (

                screener_df[
                    "Symbol"
                ]

                .head(3)

                .tolist()
            )

        # ======================================
        # MARKET BIAS
        # ======================================

        market_bias = (
            "DEFENSIVE"
        )

        if breadth:

            score = breadth[
                "health_score"
            ]

            if score >= 75:

                market_bias = (
                    "AGGRESSIVE SWING TRADING"
                )

            elif score >= 60:

                market_bias = (
                    "BULLISH SWING TRADING"
                )

            elif score >= 40:

                market_bias = (
                    "SELECTIVE TRADING"
                )

            else:

                market_bias = (
                    "DEFENSIVE MODE"
                )

        # ======================================
        # BUILD COMMENTARY
        # ======================================

        commentary = []

        commentary.append(
            "📈 MARKET COMMENTARY"
        )

        commentary.append("")

        commentary.append(
            f"🌍 Market: "
            f"{market['status']}"
        )

        commentary.append(
            f"📊 Breadth: "
            f"{breadth['health_score']}"
            if breadth
            else
            "📊 Breadth: N/A"
        )

        commentary.append(
            f"🏭 Strongest Sector: "
            f"{strongest_sector}"
        )

        commentary.append(
            f"👑 Sector Leader: "
            f"{sector_leader}"
        )

        commentary.append("")

        commentary.append(
            f"🎯 Trading Bias:"
        )

        commentary.append(
            f"{market_bias}"
        )

        commentary.append("")

        commentary.append(
            "🔥 Top AI Picks:"
        )

        if top_picks:

            for i, symbol in enumerate(
                top_picks,
                start=1
            ):

                commentary.append(
                    f"{i}. {symbol}"
                )

        else:

            commentary.append(
                "No strong setup today"
            )

        commentary.append("")

        commentary.append(
            "🤖 AI Stock Screener Indonesia"
        )

        return "\n".join(commentary)

    except Exception as e:

        print(
            f"MARKET COMMENTARY ERROR: "
            f"{e}"
        )

        return (
            "❌ Failed to generate "
            "market commentary"
        )