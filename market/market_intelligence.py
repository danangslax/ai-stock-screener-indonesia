from infrastructure.logger import logger

# ======================================
# MARKET COMMENTARY TEMPLATES
# ======================================

MARKET_TEMPLATES = {
    "STRONG_BULL": {
        "emoji": "🚀",
        "insight": ("Momentum market kuat " "dan breakout success tinggi."),
        "strategy": ("Breakout & momentum continuation."),
        "warning": ("Hindari entry terlalu jauh " "dari support."),
        "exposure": ("Aggressive exposure allowed."),
    },
    "BULL": {
        "emoji": "📈",
        "insight": ("Trend market sehat " "dengan leadership jelas."),
        "strategy": ("Pullback buy pada saham leader."),
        "warning": ("Jangan chase candle extended."),
        "exposure": ("Normal bullish exposure."),
    },
    "ACCUMULATION": {
        "emoji": "🛒",
        "insight": ("Market mulai akumulasi " "namun breakout belum konsisten."),
        "strategy": ("Buy near support " "dan fokus volume accumulation."),
        "warning": ("Hindari breakout agresif."),
        "exposure": ("Selective exposure."),
    },
    "SIDEWAYS": {
        "emoji": "↔️",
        "insight": ("Market bergerak dalam range."),
        "strategy": ("Swing pendek support-resistance."),
        "warning": ("Breakout rawan fake move."),
        "exposure": ("Reduced exposure."),
    },
    "DISTRIBUTION": {
        "emoji": "⚠️",
        "insight": ("Market menunjukkan " "tanda pelemahan."),
        "strategy": ("Selective trading " "dan defensive setup."),
        "warning": ("Kurangi agresivitas posisi."),
        "exposure": ("Defensive exposure."),
    },
    "PANIC": {
        "emoji": "🩸",
        "insight": ("Volatilitas tinggi " "dan market panic."),
        "strategy": ("Capital preservation."),
        "warning": ("Hindari overtrading."),
        "exposure": ("High cash allocation."),
    },
    "BEARISH": {
        "emoji": "🐻",
        "insight": ("Trend market masih lemah."),
        "strategy": ("Quick swing dan defensive."),
        "warning": ("Prioritaskan cash management."),
        "exposure": ("Low exposure."),
    },
    "RECOVERY": {
        "emoji": "🌱",
        "insight": ("Market mulai recovery " "dan leader baru muncul."),
        "strategy": ("Early trend following."),
        "warning": ("Tetap selektif pada volume."),
        "exposure": ("Gradual position building."),
    },
}

# ======================================
# GENERATE MARKET INTELLIGENCE
# ======================================


def generate_market_intelligence(snapshot):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not snapshot:

            return "⚠️ Snapshot unavailable"

        # ======================================
        # SNAPSHOT DATA
        # ======================================

        market_status = snapshot.get("market_status", "UNKNOWN")

        breadth_score = snapshot.get("breadth_score", 0)

        strongest_sector = snapshot.get("strongest_sector", "N/A")

        sector_leader = snapshot.get("sector_leader", "N/A")

        market_bias = snapshot.get("market_bias", "DEFENSIVE")

        # ======================================
        # TEMPLATE
        # ======================================

        template = MARKET_TEMPLATES.get(
            market_status,
            {
                "emoji": "❓",
                "insight": ("Market condition unclear."),
                "strategy": ("Wait and observe."),
                "warning": ("Avoid aggressive trading."),
                "exposure": ("Minimal exposure."),
            },
        )

        # ======================================
        # COMMENTARY
        # ======================================

        commentary = f"""
{template["emoji"]} MARKET REGIME:
{market_status}

📊 Breadth Score:
{breadth_score}

🏭 Strongest Sector:
{strongest_sector}

👑 Sector Leader:
{sector_leader}

🎯 Market Bias:
{market_bias}

🧠 Market Insight:
{template["insight"]}

⚠️ Market Warning:
{template["warning"]}

🔥 Best Strategy:
{template["strategy"]}

💼 Portfolio Exposure:
{template["exposure"]}
"""

        logger.info("Market intelligence generated")

        return commentary

    except Exception as e:

        logger.error(f"Market intelligence " f"error: {e}")

        return "⚠️ Intelligence unavailable"
