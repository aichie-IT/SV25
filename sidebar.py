import streamlit as st

st.set_page_config(page_title="Motor Accident Severity", layout="wide")

# Define Pages
home = st.Page("home.py", title="🏠 Home", icon=":material/home:")

overview = st.Page("overview.py", title="⚙️ General Overview", icon=":material/insights:")
factors = st.Page("factors.py", title="📊 Accident Factors", icon=":material/bar_chart:")
numerical = st.Page("numerical.py", title="📈 Numerical Analysis", icon=":material/analytics:")
advanced = st.Page("advanced.py", title="📉 Advanced Visualizations", icon=":material/show_chart:")
correlation = st.Page("correlation.py", title="🗺️ Correlation Insights", icon=":material/share:")
behavior = st.Page("behavior.py", title="🏍️ Riding Behavior Insights", icon=":material/pedal_bike:")

# Sidebar Navigation
pg = st.navigation({
    "🏠 Home": [home],
    "🏍️ Motor Accident Severity Analysis": [
        overview,
        factors,
        numerical,
        advanced,
        correlation,
        behavior
    ]
})

# Run navigation
pg.run()
