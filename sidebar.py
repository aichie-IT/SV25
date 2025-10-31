import streamlit as st

st.set_page_config(page_title="Motor Accident Severity", layout="wide")

# Define each tab as its own page entry
overview = st.Page("main.py", title="⚙️ General Overview", icon=":material/insights:", default=True)
factors = st.Page("main.py", title="📊 Accident Factors", icon=":material/bar_chart:")
numerical = st.Page("main.py", title="📈 Numerical Analysis", icon=":material/safety_check:")
advanced = st.Page("main.py", title="📉 Advanced Visualizations", icon=":material/description:")
correlation = st.Page("main.py", title="🗺️ Correlation Insights", icon=":material/safety_check:")
behavior = st.Page("main.py", title="🏍️ Riding Behavior Insights", icon=":material/description:")
home = st.Page("home.py", title="Homepage", icon=":material/home:")

pg = st.navigation({
    "🏠 Home": [home],
    "🏍️ Motor Accident Severity Analysis": ["⚙️ General Overview", "📊 Accident Factors", "📈 Numerical Analysis", "📉 Advanced Visualizations", "🗺️ Correlation Insights", "🏍️ Riding Behavior Insights"],
})

# Save current selected tab to session_state
st.session_state["current_tab"] = pg.run()
