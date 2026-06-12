import streamlit as st

# ======================================
# DEFAULT SESSION STATE
# ======================================

DEFAULT_STATE = {
    "market_snapshot": None,
    "screener_results": None,
    "selected_symbol": None,
    "selected_strategy": None,
    "selected_market": None,
    "portfolio_data": None,
    "analytics_data": None,
    "forward_testing_data": None,
    "backtest_results": None,
    "system_health": None,
    "refresh_data": False,
    "last_update": None,
}

# ======================================
# INITIALIZE SESSION STATE
# ======================================


def initialize_session_state():

    try:

        for (
            key,
            value,
        ) in DEFAULT_STATE.items():

            if key not in st.session_state:

                st.session_state[key] = value

    except Exception as e:

        print(f"❌ State init error: {e}")


# ======================================
# SET SESSION VALUE
# ======================================


def set_state(
    key,
    value,
):

    try:

        st.session_state[key] = value

        return True

    except Exception as e:

        print(f"❌ Set state error: {e}")

        return False


# ======================================
# GET SESSION VALUE
# ======================================


def get_state(
    key,
    default=None,
):

    try:

        return st.session_state.get(
            key,
            default,
        )

    except Exception as e:

        print(f"❌ Get state error: {e}")

        return default


# ======================================
# CLEAR SESSION VALUE
# ======================================


def clear_state(
    key,
):

    try:

        if key in st.session_state:

            del st.session_state[key]

        return True

    except Exception as e:

        print(f"❌ Clear state error: {e}")

        return False


# ======================================
# CLEAR ALL STATES
# ======================================


def clear_all_states():

    try:

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        return True

    except Exception as e:

        print(f"❌ Clear all state error: {e}")

        return False


# ======================================
# REFRESH FLAG
# ======================================


def trigger_refresh():

    try:

        st.session_state["refresh_data"] = True

    except Exception as e:

        print(f"❌ Refresh trigger error: {e}")


# ======================================
# RESET REFRESH FLAG
# ======================================


def reset_refresh():

    try:

        st.session_state["refresh_data"] = False

    except Exception as e:

        print(f"❌ Refresh reset error: {e}")


# ======================================
# CHECK REFRESH
# ======================================


def should_refresh():

    try:

        return st.session_state.get(
            "refresh_data",
            False,
        )

    except Exception as e:

        print(f"❌ Refresh check error: {e}")

        return False


# ======================================
# SAVE MARKET SNAPSHOT
# ======================================


def save_market_snapshot(
    snapshot,
):

    try:

        st.session_state["market_snapshot"] = snapshot

    except Exception as e:

        print(f"❌ Save snapshot error: {e}")


# ======================================
# LOAD MARKET SNAPSHOT
# ======================================


def load_market_snapshot():

    try:

        return st.session_state.get(
            "market_snapshot",
            None,
        )

    except Exception as e:

        print(f"❌ Load snapshot error: {e}")

        return None


# ======================================
# SAVE SCREENER RESULTS
# ======================================


def save_screener_results(
    screener_df,
):

    try:

        st.session_state["screener_results"] = screener_df

    except Exception as e:

        print(f"❌ Save screener error: {e}")


# ======================================
# LOAD SCREENER RESULTS
# ======================================


def load_screener_results():

    try:

        return st.session_state.get(
            "screener_results",
            None,
        )

    except Exception as e:

        print(f"❌ Load screener error: {e}")

        return None


# ======================================
# SAVE PORTFOLIO DATA
# ======================================


def save_portfolio_data(
    portfolio_data,
):

    try:

        st.session_state["portfolio_data"] = portfolio_data

    except Exception as e:

        print(f"❌ Save portfolio error: {e}")


# ======================================
# LOAD PORTFOLIO DATA
# ======================================


def load_portfolio_data():

    try:

        return st.session_state.get(
            "portfolio_data",
            None,
        )

    except Exception as e:

        print(f"❌ Load portfolio error: {e}")

        return None


# ======================================
# SAVE ANALYTICS DATA
# ======================================


def save_analytics_data(
    analytics_data,
):

    try:

        st.session_state["analytics_data"] = analytics_data

    except Exception as e:

        print(f"❌ Save analytics error: {e}")


# ======================================
# LOAD ANALYTICS DATA
# ======================================


def load_analytics_data():

    try:

        return st.session_state.get(
            "analytics_data",
            None,
        )

    except Exception as e:

        print(f"❌ Load analytics error: {e}")

        return None


# ======================================
# SAVE BACKTEST RESULTS
# ======================================


def save_backtest_results(
    stats,
):

    try:

        st.session_state["backtest_results"] = stats

    except Exception as e:

        print(f"❌ Save backtest error: {e}")


# ======================================
# LOAD BACKTEST RESULTS
# ======================================


def load_backtest_results():

    try:

        return st.session_state.get(
            "backtest_results",
            None,
        )

    except Exception as e:

        print(f"❌ Load backtest error: {e}")

        return None


# ======================================
# SAVE FORWARD TEST DATA
# ======================================


def save_forward_testing_data(
    data,
):

    try:

        st.session_state["forward_testing_data"] = data

    except Exception as e:

        print(f"❌ Save forward data error: {e}")


# ======================================
# LOAD FORWARD TEST DATA
# ======================================


def load_forward_testing_data():

    try:

        return st.session_state.get(
            "forward_testing_data",
            None,
        )

    except Exception as e:

        print(f"❌ Load forward data error: {e}")

        return None


# ======================================
# SAVE SYSTEM HEALTH
# ======================================


def save_system_health(
    health,
):

    try:

        st.session_state["system_health"] = health

    except Exception as e:

        print(f"❌ Save system health error: {e}")


# ======================================
# LOAD SYSTEM HEALTH
# ======================================


def load_system_health():

    try:

        return st.session_state.get(
            "system_health",
            None,
        )

    except Exception as e:

        print(f"❌ Load system health error: {e}")

        return None
