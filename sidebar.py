import streamlit as st

st.set_page_config(
    page_title="Motor Accident Severity"
)

# --- Sidebar Logo ---
st.sidebar.markdown(
    """
    <div style='text-align:center; margin-bottom:15px;'>
        <img src='https://cdn-icons-png.flaticon.com/512/743/743922.png' width='100'>
    </div>
    """,
    unsafe_allow_html=True
)


visualise = st.Page('main.py', title='Motor Accident Severity Analysis', icon=":material/motor:")

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()
