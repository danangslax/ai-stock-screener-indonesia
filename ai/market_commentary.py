# ======================================
# GENERATE MARKET COMMENTARY
# ======================================


def generate_market_commentary(snapshot, screener_df=None):

    try:

        # ======================================
        # TOP PICKS
        # ======================================

        top_picks = []

        if screener_df is not None and not screener_df.empty:

            top_picks = screener_df["Symbol"].head(3).tolist()

        # ======================================
        # BUILD COMMENTARY
        # ======================================

        commentary = []

        commentary.append("📈 MARKET COMMENTARY")

        commentary.append("")

        commentary.append(f"🌍 Market: " f"{snapshot['market_status']}")

        commentary.append(f"📊 Breadth Score: " f"{snapshot['breadth_score']}")

        commentary.append(f"🏭 Strongest Sector: " f"{snapshot['strongest_sector']}")

        commentary.append(f"👑 Sector Leader: " f"{snapshot['sector_leader']}")

        commentary.append("")

        commentary.append(f"🎯 Market Bias:")

        commentary.append(f"{snapshot['market_bias']}")

        commentary.append("")

        commentary.append("🔥 Top AI Picks:")

        if top_picks:

            for i, symbol in enumerate(top_picks, start=1):

                commentary.append(f"{i}. {symbol}")

        else:

            commentary.append("No strong setup today")

        commentary.append("")

        commentary.append("🤖 AI Stock Screener Indonesia")

        return "\n".join(commentary)

    except Exception as e:

        print(f"COMMENTARY ERROR: " f"{e}")

        return "❌ Failed to generate " "market commentary"
