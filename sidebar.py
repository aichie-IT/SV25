import streamlit as st
from st_pages import Page, navigation

# --- PAGE CONFIG ---
st.set_page_config(page_title="Motor Accident Severity", layout="wide")

# --- SIDEBAR LOGO ---
st.sidebar.markdown(
    """
    <div style='text-align:center; margin-bottom:10px;'>
        <img src='https://cdn-icons-png.flaticon.com/512/743/743922.png' width='100'>
    </div>
    <div style='text-align:center; font-size:14px; color:gray; margin-bottom:20px;'>
        Interactive Accident Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

# --- NAVIGATION PAGES ---
home = Page('home.py', title='Homepage', default=True, icon=":material/home:")
visualise = Page('main.py', title='Motor Accident Severity Analysis', icon=":material/school:")

pg = navigation(
    {
        "Menu": [home, visualise]
    }
)

# --- SIDEBAR FOOTER (Optional) ---
st.sidebar.markdown(
    "<div style='text-align:center; font-size:12px; color:gray; margin-top:20px;'>© 2025 Motor Accident Dashboard</div>",
    unsafe_allow_html=True
)
pg.run()
