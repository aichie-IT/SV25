import streamlit as st

st.sidebar.title("Navigation")

main_page = st.sidebar.radio(
    "Go to:",
    ["Home", "Motor Accident Severity Analysis"]
)

# Sub-page for Motor Accident
sub_page = None
if main_page == "Motor Accident Severity Analysis":
    sub_page = st.sidebar.radio(
        "Select Section:",
        ["Overview", "Accident Factors", "Riding Behavior", "Summary"]
    )
