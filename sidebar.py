import streamlit as st

def sidebar_navigation(df):
    """
    Sidebar navigation for the app.
    Returns:
        page (str): Selected main page
        tab_selection (str): Selected tab within the Motor Accident section
    """

    # --- Main Navigation ---
    st.sidebar.title("📂 Navigation")
    page = st.sidebar.radio(
        "Main Menu:",
        ["🏠 Home", "🏍️ Motor Accident Severity Analysis"]
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
            key="sidebar_tab"
        )

    # --- Optional: Dataset Summary ---
    if df is not None:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🧾 Data Summary")
        st.sidebar.info(
            f"**Total Records:** {len(df):,}\n"
            f"**Columns:** {len(df.columns)}"
        )

    return page, tab_selection
