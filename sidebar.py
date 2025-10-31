import streamlit as st

def sidebar_navigation(df):
    """
    Returns (page, selected_section)
    - page: "🏠 Home" or "🏍️ Motor Accident Severity Analysis"
    - selected_section: one of the section names (or None)
    """

    # initialize session state key for the active section
    if "active_section" not in st.session_state:
        st.session_state.active_section = "⚙️ General Overview"

    st.sidebar.title("📂 Navigation")
    page = st.sidebar.radio(
        "Main Menu:",
        ["🏠 Home", "🏍️ Motor Accident Severity Analysis"],
        index=0,
        key="main_menu"
    )

    # if Analysis page chosen, show sub-sections
    if page == "🏍️ Motor Accident Severity Analysis":
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Dashboard Sections")

        # Sidebar radio updates the session-state active_section
        st.sidebar.radio(
            "Go to Section:",
            [
                "⚙️ General Overview",
                "📊 Accident Factors",
                "📈 Numerical Analysis",
                "📉 Advanced Visualizations",
                "🗺️ Correlation Insights",
                "🏍️ Riding Behavior Insights"
            ],
            index=[
                "⚙️ General Overview",
                "📊 Accident Factors",
                "📈 Numerical Analysis",
                "📉 Advanced Visualizations",
                "🗺️ Correlation Insights",
                "🏍️ Riding Behavior Insights"
            ].index(st.session_state.active_section),
            key="sidebar_tab",
            on_change=lambda: st.session_state.update({"active_section": st.session_state.sidebar_tab})
        )

    # optional dataset summary
    if df is not None:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🧾 Data Summary")
        st.sidebar.info(
            f"**Total Records:** {len(df):,}\n**Columns:** {len(df.columns)}"
        )

    return page, st.session_state.active_section
