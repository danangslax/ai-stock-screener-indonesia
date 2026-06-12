# ======================================
# AI MARKET INTELLIGENCE
# ======================================


def generate_market_intelligence(snapshot):

    try:

        if not snapshot:

            return "⚠️ Snapshot unavailable"

        market_status = snapshot.get("market_status", "UNKNOWN")

        breadth_score = snapshot.get("breadth_score", 0)

        strongest_sector = snapshot.get("strongest_sector", "N/A")

        sector_leader = snapshot.get("sector_leader", "N/A")

        market_bias = snapshot.get("market_bias", "DEFENSIVE")

        # ======================================
        # MARKET INSIGHT
        # ======================================

        insight = ""

        strategy = ""

        warning = ""

        # ======================================
        # STRONG BULL
        # ======================================

        if market_status == "STRONG_BULL":

            insight = "Momentum market kuat " "dan breakout success tinggi."

            strategy = "Breakout & momentum continuation."

            warning = "Hindari entry terlalu jauh " "dari support."

        # ======================================
        # BULL
        # ======================================

        elif market_status == "BULL":

            insight = "Trend market sehat " "dengan leadership jelas."

            strategy = "Pullback buy pada saham leader."

            warning = "Jangan chase candle extended."

        # ======================================
        # ACCUMULATION
        # ======================================

        elif market_status == "ACCUMULATION":

            insight = "Market mulai akumulasi " "namun breakout belum konsisten."

            strategy = "Buy near support " "dan fokus volume accumulation."

            warning = "Hindari breakout agresif."

        # ======================================
        # SIDEWAYS
        # ======================================

        elif market_status == "SIDEWAYS":

            insight = "Market bergerak dalam range."

            strategy = "Swing pendek support-resistance."

            warning = "Breakout rawan fake move."

        # ======================================
        # DISTRIBUTION
        # ======================================

        elif market_status == "DISTRIBUTION":

            insight = "Market menunjukkan " "tanda pelemahan."

            strategy = "Selective trading " "dan defensive setup."

            warning = "Kurangi agresivitas posisi."

        # ======================================
        # PANIC
        # ======================================

        elif market_status == "PANIC":

            insight = "Volatilitas tinggi " "dan market panic."

            strategy = "Capital preservation."

            warning = "Hindari overtrading."

        # ======================================
        # BEARISH
        # ======================================

        elif market_status == "BEARISH":

            insight = "Trend market masih lemah."

            strategy = "Quick swing dan defensive."

            warning = "Prioritaskan cash management."

        # ======================================
        # RECOVERY
        # ======================================

        elif market_status == "RECOVERY":

            insight = "Market mulai recovery " "dan leader baru muncul."

            strategy = "Early trend following."

            warning = "Tetap selektif pada volume."

        # ======================================
        # FINAL COMMENTARY
        # ======================================

        commentary = f"""
📈 MARKET REGIME: {market_status}

📊 Breadth Score:
{breadth_score}

🏭 Strongest Sector:
{strongest_sector}

👑 Sector Leader:
{sector_leader}

🎯 Market Bias:
{market_bias}

🧠 Market Insight:
{insight}

⚠️ Market Warning:
{warning}

🔥 Best Strategy:
{strategy}
"""

        return commentary

    except Exception as e:

        print(f"❌ Market intelligence error: " f"{e}")

        return "⚠️ Intelligence unavailable"
