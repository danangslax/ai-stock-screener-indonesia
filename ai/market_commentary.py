from infrastructure.logger import logger

# ======================================
# GENERATE MARKET COMMENTARY
# ======================================


def generate_market_commentary(snapshot, screener_df=None):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not snapshot:

            logger.warning("Market commentary " "received empty snapshot")

            return "⚠️ Market snapshot " "unavailable"

        # ======================================
        # SNAPSHOT DATA
        # ======================================

        market_status = snapshot.get("market_status", "UNKNOWN")

        breadth_score = snapshot.get("breadth_score", 0)

        strongest_sector = snapshot.get("strongest_sector", "N/A")

        sector_leader = snapshot.get("sector_leader", "N/A")

        market_bias = snapshot.get("market_bias", "DEFENSIVE")

        # ======================================
        # TOP PICKS
        # ======================================

        top_picks = []

        if screener_df is not None and not screener_df.empty:

            top_rows = screener_df.head(3)

            for _, row in top_rows.iterrows():

                top_picks.append(
                    {
                        "symbol": row.get("Symbol", "N/A"),
                        "confidence": row.get("Confidence", 0),
                        "strategy": row.get("Strategy", "N/A"),
                    }
                )

        # ======================================
        # MARKET INSIGHT
        # ======================================

        insight = ""

        warning = ""

        action = ""

        # ======================================
        # REGIME LOGIC
        # ======================================

        if market_status == "STRONG_BULL":

            insight = (
                "Momentum market sangat kuat "
                "dan breakout memiliki "
                "probabilitas sukses tinggi."
            )

            warning = "Hindari entry terlalu jauh " "dari support."

            action = "Fokus pada breakout " "dan momentum leaders."

        elif market_status == "BULL":

            insight = "Trend market sehat " "dengan leadership jelas."

            warning = "Jangan chase candle " "yang terlalu extended."

            action = "Prioritaskan saham " "dengan volume kuat."

        elif market_status == "SIDEWAYS":

            insight = "Market bergerak " "dalam range."

            warning = "Breakout rawan fake move."

            action = "Gunakan pendekatan " "swing support-resistance."

        elif market_status == "BEARISH":

            insight = "Tekanan market " "masih cukup besar."

            warning = "Kurangi agresivitas " "dan exposure."

            action = "Prioritaskan defensive " "setup dan cash."

        elif market_status == "PANIC":

            insight = "Volatilitas tinggi " "dan market panic."

            warning = "Capital preservation " "lebih penting " "daripada profit."

            action = "Kurangi posisi " "dan hindari overtrading."

        elif market_status == "RECOVERY":

            insight = "Market mulai recovery " "dan leader baru muncul."

            warning = "Recovery belum sepenuhnya " "stabil."

            action = "Fokus pada early trend " "dan saham strongest sector."

        else:

            insight = "Kondisi market " "masih netral."

            warning = "Tetap disiplin " "risk management."

            action = "Selective trading."

        # ======================================
        # BUILD COMMENTARY
        # ======================================

        commentary = []

        commentary.append("📈 MARKET COMMENTARY")

        commentary.append("")

        commentary.append(f"🌍 Market Regime: " f"{market_status}")

        commentary.append(f"📊 Breadth Score: " f"{breadth_score}")

        commentary.append(f"🏭 Strongest Sector: " f"{strongest_sector}")

        commentary.append(f"👑 Sector Leader: " f"{sector_leader}")

        commentary.append("")

        commentary.append(f"🎯 Market Bias:")

        commentary.append(f"{market_bias}")

        commentary.append("")

        commentary.append("🧠 AI Market Insight:")

        commentary.append(insight)

        commentary.append("")

        commentary.append("⚠️ Risk Warning:")

        commentary.append(warning)

        commentary.append("")

        commentary.append("🔥 Suggested Action:")

        commentary.append(action)

        commentary.append("")

        commentary.append("🚀 Top AI Picks:")

        # ======================================
        # TOP PICKS
        # ======================================

        if top_picks:

            for i, pick in enumerate(top_picks, start=1):

                commentary.append(
                    f"{i}. "
                    f"{pick['symbol']} "
                    f"| Confidence: "
                    f"{pick['confidence']} "
                    f"| Strategy: "
                    f"{pick['strategy']}"
                )

        else:

            commentary.append("No strong setup today")

        commentary.append("")

        commentary.append("🤖 AI Stock Screener Indonesia")

        logger.info("Market commentary generated")

        return "\n".join(commentary)

    except Exception as e:

        logger.error(f"Commentary error: " f"{e}")

        return "❌ Failed to generate " "market commentary"
