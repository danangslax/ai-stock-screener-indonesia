import os
import psutil
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from pathlib import Path

from infrastructure.cache_validator import (
    validate_all_cache,
)

from infrastructure.snapshot_loader import (
    load_market_snapshot,
)

from ai.ai_parameters import (
    load_parameters,
)

# ======================================
# SYSTEM HEALTH DASHBOARD PAGE
# ======================================


def render_system_health_dashboard():

    st.header("🛠️ System Health Dashboard")

    # ======================================
    # SYSTEM METRICS
    # ======================================

    st.subheader("💻 System Resources")

    cpu_usage = psutil.cpu_percent()

    memory = psutil.virtual_memory()

    disk = psutil.disk_usage("/")

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "CPU Usage",
            f"{cpu_usage}%",
        )

    with m2:

        st.metric(
            "Memory Usage",
            f"{memory.percent}%",
        )

    with m3:

        st.metric(
            "Disk Usage",
            f"{disk.percent}%",
        )

    # ======================================
    # RESOURCE CHART
    # ======================================

    st.subheader("📊 Resource Usage")

    resource_fig = go.Figure()

    resource_fig.add_trace(
        go.Bar(
            x=[
                "CPU",
                "Memory",
                "Disk",
            ],
            y=[
                cpu_usage,
                memory.percent,
                disk.percent,
            ],
            name="Usage %",
        )
    )

    resource_fig.update_layout(
        height=400,
        template="plotly_dark",
        title="System Resource Usage",
    )

    st.plotly_chart(
        resource_fig,
        use_container_width=True,
    )

    # ======================================
    # CACHE VALIDATION
    # ======================================

    st.subheader("🗂️ Cache Validation")

    cache_summary = validate_all_cache()

    total_cache = cache_summary.get(
        "total",
        0,
    )

    valid_cache = cache_summary.get(
        "valid",
        0,
    )

    invalid_cache = cache_summary.get(
        "invalid",
        0,
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Total Cache",
            total_cache,
        )

    with c2:

        st.metric(
            "Valid Cache",
            valid_cache,
        )

    with c3:

        st.metric(
            "Invalid Cache",
            invalid_cache,
        )

    # ======================================
    # CACHE STATUS
    # ======================================

    if invalid_cache == 0:

        st.success("✅ Cache system healthy")

    else:

        st.warning(f"⚠️ {invalid_cache} invalid cache files detected")

    # ======================================
    # INVALID FILES
    # ======================================

    invalid_files = cache_summary.get(
        "invalid_files",
        [],
    )

    if invalid_files:

        st.subheader("❌ Invalid Cache Files")

        invalid_df = pd.DataFrame({"Invalid Files": invalid_files})

        st.dataframe(
            invalid_df,
            use_container_width=True,
        )

    # ======================================
    # MARKET SNAPSHOT
    # ======================================

    st.subheader("🌍 Market Snapshot Status")

    snapshot = load_market_snapshot()

    if snapshot:

        st.success("✅ Market snapshot available")

        snapshot_df = pd.DataFrame(
            [
                {
                    "Metric": key,
                    "Value": value,
                }
                for key, value in snapshot.items()
            ]
        )

        st.dataframe(
            snapshot_df,
            use_container_width=True,
        )

    else:

        st.warning("⚠️ Market snapshot unavailable")

    # ======================================
    # AI PARAMETERS
    # ======================================

    st.subheader("🤖 AI Parameters")

    parameters = load_parameters()

    parameter_df = pd.DataFrame(
        [
            {
                "Parameter": key,
                "Value": value,
            }
            for key, value in parameters.items()
        ]
    )

    st.dataframe(
        parameter_df,
        use_container_width=True,
    )

    # ======================================
    # DATA DIRECTORY
    # ======================================

    st.subheader("📁 Storage Information")

    data_dir = Path("data")

    total_files = 0

    total_size = 0

    if data_dir.exists():

        for path in data_dir.rglob("*"):

            if path.is_file():

                total_files += 1

                total_size += path.stat().st_size

    total_size_mb = round(
        total_size / (1024 * 1024),
        2,
    )

    s1, s2 = st.columns(2)

    with s1:

        st.metric(
            "Total Files",
            total_files,
        )

    with s2:

        st.metric(
            "Storage Size",
            f"{total_size_mb} MB",
        )

    # ======================================
    # DIRECTORY BREAKDOWN
    # ======================================

    st.subheader("📂 Directory Breakdown")

    directory_stats = []

    if data_dir.exists():

        for item in data_dir.iterdir():

            if item.is_dir():

                file_count = 0

                folder_size = 0

                for file in item.rglob("*"):

                    if file.is_file():

                        file_count += 1

                        folder_size += file.stat().st_size

                directory_stats.append(
                    {
                        "Directory": item.name,
                        "Files": file_count,
                        "Size_MB": round(
                            folder_size / (1024 * 1024),
                            2,
                        ),
                    }
                )

    if directory_stats:

        directory_df = pd.DataFrame(directory_stats)

        st.dataframe(
            directory_df,
            use_container_width=True,
        )

    # ======================================
    # DIRECTORY CHART
    # ======================================

    if directory_stats:

        dir_chart_df = pd.DataFrame(directory_stats)

        dir_fig = go.Figure()

        dir_fig.add_trace(
            go.Bar(
                x=dir_chart_df["Directory"],
                y=dir_chart_df["Size_MB"],
                name="Storage",
            )
        )

        dir_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Directory Storage Usage",
        )

        st.plotly_chart(
            dir_fig,
            use_container_width=True,
        )

    # ======================================
    # ENVIRONMENT VARIABLES
    # ======================================

    st.subheader("🔐 Environment Status")

    env_variables = [
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
    ]

    env_status = []

    for variable in env_variables:

        status = "AVAILABLE" if os.getenv(variable) else "MISSING"

        env_status.append(
            {
                "Variable": variable,
                "Status": status,
            }
        )

    env_df = pd.DataFrame(env_status)

    st.dataframe(
        env_df,
        use_container_width=True,
    )

    # ======================================
    # SYSTEM STATUS
    # ======================================

    st.subheader("🚦 Overall System Status")

    issues = []

    if cpu_usage > 90:

        issues.append("High CPU usage")

    if memory.percent > 90:

        issues.append("High memory usage")

    if disk.percent > 90:

        issues.append("Low disk space")

    if invalid_cache > 0:

        issues.append("Invalid cache files")

    missing_env = [row["Variable"] for row in env_status if row["Status"] == "MISSING"]

    if missing_env:

        issues.append("Missing environment variables")

    if not issues:

        st.success("✅ System operating normally")

    else:

        for issue in issues:

            st.error(f"❌ {issue}")

    # ======================================
    # REFRESH BUTTON
    # ======================================

    st.divider()

    if st.button(
        "🔄 Refresh System Status",
        use_container_width=True,
    ):

        st.rerun()
