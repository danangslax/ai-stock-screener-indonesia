import streamlit as st

# ======================================
# PAGE CONFIG
# ======================================


def setup_page_config():

    try:

        st.set_page_config(
            page_title="AI Stock Screener Indonesia",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    except Exception as e:

        print(f"❌ Page config error: {e}")


# ======================================
# MAIN HEADER
# ======================================


def render_main_header():

    try:

        st.title("📈 AI Stock Screener Indonesia")

        st.caption("AI-Powered Swing Trading Dashboard")

        st.markdown("---")

    except Exception as e:

        st.error(f"Header error: {e}")


# ======================================
# SIDEBAR
# ======================================


def render_sidebar():

    try:

        with st.sidebar:

            st.title("🤖 AI Dashboard")

            st.markdown("---")

            st.markdown("""
### 📊 Dashboard Menu

- Stock Overview
- Market Snapshot
- Screener Dashboard
- Portfolio Dashboard
- Analytics Dashboard
- Backtest Dashboard
- AI Learning Dashboard
- Forward Testing Dashboard
- System Health Dashboard
""")

            st.markdown("---")

            st.info("AI Stock Screener Indonesia")

    except Exception as e:

        st.error(f"Sidebar error: {e}")


# ======================================
# SECTION HEADER
# ======================================


def render_section_header(
    title,
    icon="📌",
):

    try:

        st.markdown("")

        st.subheader(f"{icon} {title}")

    except Exception as e:

        st.error(f"Section header error: {e}")


# ======================================
# INFO BOX
# ======================================


def render_info_box(
    message,
):

    try:

        st.info(message)

    except Exception as e:

        st.error(f"Info box error: {e}")


# ======================================
# SUCCESS BOX
# ======================================


def render_success_box(
    message,
):

    try:

        st.success(message)

    except Exception as e:

        st.error(f"Success box error: {e}")


# ======================================
# WARNING BOX
# ======================================


def render_warning_box(
    message,
):

    try:

        st.warning(message)

    except Exception as e:

        st.error(f"Warning box error: {e}")


# ======================================
# ERROR BOX
# ======================================


def render_error_box(
    message,
):

    try:

        st.error(message)

    except Exception as e:

        print(f"❌ Error box error: {e}")


# ======================================
# EMPTY STATE
# ======================================


def render_empty_state(
    message="No data available",
):

    try:

        st.warning(message)

    except Exception as e:

        st.error(f"Empty state error: {e}")


# ======================================
# DIVIDER
# ======================================


def render_divider():

    try:

        st.markdown("---")

    except Exception as e:

        print(f"❌ Divider error: {e}")


# ======================================
# FOOTER
# ======================================


def render_footer():

    try:

        st.markdown("---")

        st.caption("🤖 AI Stock Screener Indonesia | Streamlit Dashboard")

    except Exception as e:

        st.error(f"Footer error: {e}")


# ======================================
# MARKET STATUS BANNER
# ======================================


def render_market_banner(
    market_status,
):

    try:

        banner = f"🌍 Current Market Regime: " f"{market_status}"

        if market_status in [
            "STRONG_BULL",
            "BULL",
            "RECOVERY",
        ]:

            st.success(banner)

        elif market_status in [
            "SIDEWAYS",
            "ACCUMULATION",
        ]:

            st.warning(banner)

        else:

            st.error(banner)

    except Exception as e:

        st.error(f"Market banner error: {e}")


# ======================================
# LOADING SCREEN
# ======================================


def render_loading_screen(
    message="Loading data...",
):

    try:

        with st.spinner(message):

            pass

    except Exception as e:

        st.error(f"Loading screen error: {e}")


# ======================================
# TWO COLUMN LAYOUT
# ======================================


def create_two_columns():

    try:

        return st.columns(2)

    except Exception as e:

        st.error(f"Two column error: {e}")

        return None, None


# ======================================
# THREE COLUMN LAYOUT
# ======================================


def create_three_columns():

    try:

        return st.columns(3)

    except Exception as e:

        st.error(f"Three column error: {e}")

        return None, None, None


# ======================================
# FOUR COLUMN LAYOUT
# ======================================


def create_four_columns():

    try:

        return st.columns(4)

    except Exception as e:

        st.error(f"Four column error: {e}")

        return None, None, None, None


# ======================================
# EXPANDER SECTION
# ======================================


def render_expander(
    title,
    content,
    expanded=False,
):

    try:

        with st.expander(
            title,
            expanded=expanded,
        ):

            st.write(content)

    except Exception as e:

        st.error(f"Expander error: {e}")


# ======================================
# JSON VIEWER
# ======================================


def render_json(
    data,
):

    try:

        st.json(data)

    except Exception as e:

        st.error(f"JSON render error: {e}")


# ======================================
# CODE BLOCK
# ======================================


def render_code_block(
    code,
    language="python",
):

    try:

        st.code(
            code,
            language=language,
        )

    except Exception as e:

        st.error(f"Code block error: {e}")


# ======================================
# STATUS BADGE
# ======================================


def render_status_badge(
    status,
):

    try:

        if status in [
            "GOOD",
            "STRONG",
            "HIGH",
            "PASS",
            "ROBUST",
        ]:

            st.success(status)

        elif status in [
            "NEUTRAL",
            "MEDIUM",
            "WATCH",
        ]:

            st.warning(status)

        else:

            st.error(status)

    except Exception as e:

        st.error(f"Status badge error: {e}")
