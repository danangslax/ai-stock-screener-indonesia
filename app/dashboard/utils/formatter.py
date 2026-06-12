from datetime import datetime

# ======================================
# CURRENCY FORMATTER
# ======================================


def format_currency(
    value,
    prefix="Rp",
):

    try:

        if value is None:

            return f"{prefix}0"

        formatted = f"{prefix}{value:,.0f}"

        return formatted.replace(
            ",",
            ".",
        )

    except Exception as e:

        print(f"❌ Currency format error: {e}")

        return f"{prefix}0"


# ======================================
# PERCENT FORMATTER
# ======================================


def format_percent(
    value,
    decimals=2,
):

    try:

        if value is None:

            return "0%"

        return f"{round(float(value), decimals)}%"

    except Exception as e:

        print(f"❌ Percent format error: {e}")

        return "0%"


# ======================================
# NUMBER FORMATTER
# ======================================


def format_number(
    value,
    decimals=2,
):

    try:

        if value is None:

            return "0"

        return f"{float(value):,.{decimals}f}"

    except Exception as e:

        print(f"❌ Number format error: {e}")

        return "0"


# ======================================
# PRICE FORMATTER
# ======================================


def format_price(
    price,
):

    try:

        if price is None:

            return "0"

        return f"{float(price):,.2f}"

    except Exception as e:

        print(f"❌ Price format error: {e}")

        return "0"


# ======================================
# PNL FORMATTER
# ======================================


def format_pnl(
    pnl,
):

    try:

        if pnl is None:

            return "0"

        pnl = float(pnl)

        if pnl > 0:

            return f"+{pnl:,.2f}"

        return f"{pnl:,.2f}"

    except Exception as e:

        print(f"❌ PnL format error: {e}")

        return "0"


# ======================================
# PNL PERCENT FORMATTER
# ======================================


def format_pnl_percent(
    pnl_percent,
):

    try:

        if pnl_percent is None:

            return "0%"

        pnl_percent = float(pnl_percent)

        if pnl_percent > 0:

            return f"+{pnl_percent:.2f}%"

        return f"{pnl_percent:.2f}%"

    except Exception as e:

        print(f"❌ PnL percent error: {e}")

        return "0%"


# ======================================
# MARKET STATUS FORMATTER
# ======================================


def format_market_status(
    status,
):

    try:

        if not status:

            return "UNKNOWN"

        mapping = {
            "STRONG_BULL": ("🚀 STRONG BULL"),
            "BULL": "📈 BULL",
            "ACCUMULATION": ("🟢 ACCUMULATION"),
            "SIDEWAYS": ("🟡 SIDEWAYS"),
            "DISTRIBUTION": ("🟠 DISTRIBUTION"),
            "BEARISH": ("🔴 BEARISH"),
            "PANIC": "⚠️ PANIC",
            "RECOVERY": ("💪 RECOVERY"),
        }

        return mapping.get(
            status,
            status,
        )

    except Exception as e:

        print(f"❌ Market status error: {e}")

        return "UNKNOWN"


# ======================================
# CONFIDENCE FORMATTER
# ======================================


def format_confidence(
    confidence,
):

    try:

        if confidence is None:

            return "0"

        confidence = int(confidence)

        if confidence >= 85:

            return f"🔥 {confidence}"

        if confidence >= 70:

            return f"✅ {confidence}"

        if confidence >= 50:

            return f"⚠️ {confidence}"

        return f"❌ {confidence}"

    except Exception as e:

        print(f"❌ Confidence format error: {e}")

        return "0"


# ======================================
# STRATEGY FORMATTER
# ======================================


def format_strategy(
    strategy,
):

    try:

        if not strategy:

            return "UNKNOWN"

        mapping = {
            "BREAKOUT": ("🚀 BREAKOUT"),
            "PULLBACK": ("📉 PULLBACK"),
            "DEFENSIVE": ("🛡️ DEFENSIVE"),
        }

        return mapping.get(
            strategy,
            strategy,
        )

    except Exception as e:

        print(f"❌ Strategy format error: {e}")

        return "UNKNOWN"


# ======================================
# QUALITY FORMATTER
# ======================================


def format_quality(
    quality,
):

    try:

        if not quality:

            return "UNKNOWN"

        mapping = {
            "HIGH": "🔥 HIGH",
            "MEDIUM": ("✅ MEDIUM"),
            "LOW": "⚠️ LOW",
            "EXCELLENT": ("🏆 EXCELLENT"),
            "GOOD": "👍 GOOD",
            "MODERATE": ("⚠️ MODERATE"),
            "WEAK": "❌ WEAK",
        }

        return mapping.get(
            quality,
            quality,
        )

    except Exception as e:

        print(f"❌ Quality format error: {e}")

        return "UNKNOWN"


# ======================================
# DATE FORMATTER
# ======================================


def format_date(
    value,
    date_format="%Y-%m-%d",
):

    try:

        if value is None:

            return "-"

        if isinstance(
            value,
            datetime,
        ):

            return value.strftime(date_format)

        parsed = datetime.fromisoformat(
            str(value).replace(
                "Z",
                "",
            )
        )

        return parsed.strftime(date_format)

    except Exception as e:

        print(f"❌ Date format error: {e}")

        return str(value)


# ======================================
# DATETIME FORMATTER
# ======================================


def format_datetime(
    value,
):

    try:

        return format_date(
            value,
            "%Y-%m-%d %H:%M",
        )

    except Exception as e:

        print(f"❌ Datetime format error: {e}")

        return str(value)


# ======================================
# VOLUME FORMATTER
# ======================================


def format_volume(
    volume,
):

    try:

        if volume is None:

            return "0"

        volume = float(volume)

        if volume >= 1_000_000_000:

            return f"{volume / 1_000_000_000:.2f}B"

        if volume >= 1_000_000:

            return f"{volume / 1_000_000:.2f}M"

        if volume >= 1_000:

            return f"{volume / 1_000:.2f}K"

        return str(int(volume))

    except Exception as e:

        print(f"❌ Volume format error: {e}")

        return "0"


# ======================================
# BOOLEAN FORMATTER
# ======================================


def format_boolean(
    value,
):

    try:

        if value:

            return "✅ YES"

        return "❌ NO"

    except Exception as e:

        print(f"❌ Boolean format error: {e}")

        return "❌ NO"


# ======================================
# STATUS COLOR FORMATTER
# ======================================


def get_status_color(
    status,
):

    try:

        positive = [
            "HIGH",
            "GOOD",
            "STRONG",
            "PASS",
            "ROBUST",
            "BULL",
            "STRONG_BULL",
        ]

        neutral = [
            "MEDIUM",
            "WATCH",
            "SIDEWAYS",
            "NEUTRAL",
        ]

        if status in positive:

            return "green"

        if status in neutral:

            return "orange"

        return "red"

    except Exception as e:

        print(f"❌ Status color error: {e}")

        return "gray"
