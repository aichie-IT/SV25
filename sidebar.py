import streamlit as st

def sidebar_navigation(df):
    """
    Returns the selected main page and the selected tab
    """

    # --- Main Page Selection ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page:",
        ["🏠 Home", "🏍️ Motor Accident Severity Analysis"]
    )

    tab_selection = None
    if page == "🏍️ Motor Accident Severity Analysis":
        st.sidebar.markdown("---")
        st.sidebar.subheader("📌 Dashboard Sections")
        tab_selection = st.sidebar.radio(
            "Select Section:",
            ["⚙️ General Overview", "📊 Accident Factors", "📈 Numerical Analysis",
             "📉 Advanced Visualizations", "🗺️ Correlation Insights", "🏍️ Riding Behavior Insights"]
        )

    # --- Optional: Data Summary ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧾 Data Summary")
    st.sidebar.info(f"**Total Records:** {len(df):,}\n**Columns:** {len(df.columns)}")

    return page, tab_selection
