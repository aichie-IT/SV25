import streamlit as st

# Set overall page configuration once
st.set_page_config(
    page_title="Scientific Visualization Portal",
    layout="wide",
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to page:",
    ["🏠 Home", "📊 Student Data Visualization"]
)
if "Home" in page:
    from home import *
else:
    from main import *
