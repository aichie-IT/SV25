import streamlit as st

st.set_page_config(page_title="Motor Accident Severity", layout="wide")

# Define each tab as its own page entry
overview = st.Page("main.py", title="Overview", icon=":material/insights:", default=True)
factors = st.Page("main.py", title="Accident Factors", icon=":material/bar_chart:")
behavior = st.Page("main.py", title="Riding Behavior", icon=":material/safety_check:")
summary = st.Page("main.py", title="Summary", icon=":material/description:")
home = st.Page("home.py", title="Homepage", icon=":material/home:")

pg = st.navigation({
    "🏠 Home": [home],
    "🏍️ Motor Accident Severity Analysis": [overview, factors, behavior, summary],
})

# Save current selected tab to session_state
st.session_state["current_tab"] = pg.run()
