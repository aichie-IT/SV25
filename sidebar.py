import streamlit as st

def sidebar_navigation(df):
    """
    Sidebar navigation for the app.
    Returns:
        page (str): Selected main page
        tab_selection (str): Selected tab within the Motor Accident section
    """

    # Initialize session state for tab synchronization
    if "tab_selection" not in st.session_state:
        st.session_state.tab_selection = "⚙️ General Overview"

    # --- Main Navigation ---
    st.sidebar.title("📂 Navigation")
    page = st.sidebar.radio(
        "Main Menu:",
        ["🏠 Home", "🏍️ Motor Accident Severity Analysis"],
        key="main_menu"
    )

    # --- Sub-navigation for Analysis Page ---
    tab_selection = None
    if page == "🏍️ Motor Accident Severity Analysis":
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Dashboard Sections")
        tab_selection = st.sidebar.radio(
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
            ].index(st.session_state.tab_selection),
            key="sidebar_tab",
            on_change=lambda: st.session_state.update(
                {"tab_selection": st.session_state.sidebar_tab}
            )
        )

    # --- Optional: Dataset Summary ---
    if df is not None:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🧾 Data Summary")
        st.sidebar.info(
            f"**Total Records:** {len(df):,}\n"
            f"**Columns:** {len(df.columns)}"
        )

    return page, st.session_state.tab_selection
