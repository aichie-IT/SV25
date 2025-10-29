import streamlit as st

# ====== SIDEBAR ======
with st.sidebar:
    # --- Centered Logo ---
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 10px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/743/743922.png' width='100'>
        </div>
        """, unsafe_allow_html=True
    )

    # --- Dashboard Title ---
    st.markdown("<h2 style='text-align:center'>Motorbike Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: gray; margin-top:-10px;'>Interactive Accident Insights</p>", unsafe_allow_html=True)
    st.markdown("---")

# ===== THEME TOGGLE =====
theme_mode = st.sidebar.radio("Select Theme Mode", ["Light 🌞", "Dark 🌙"], horizontal=True)

if theme_mode == "Dark 🌙":
    st.markdown("""
        <style>
        body { background-color: #121212; color: white; }
        [data-testid="stSidebar"] { background-color: #1E1E1E; color: white; }
        .stMetric, .stPlotlyChart, .stMarkdown { color: white !important; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body { background-color: #FAFAFA; color: black; }
        [data-testid="stSidebar"] { background-color: #FFFFFF; color: black; }
        </style>
    """, unsafe_allow_html=True)

# ===== COLOR THEME =====
color_theme = px.colors.qualitative.Pastel

# Add a banner image at the top
banner_image = 'https://raw.githubusercontent.com/fakhitah3/FHPK-TVET/main/3u1i.jpeg'
st.image(banner_image, use_container_width=True)

# Add the main introduction paragraph
st.write(
    """
    **Scientific Visualization** is a multidisciplinary field that focuses on transforming complex scientific data into visual forms that are easier to understand, interpret, and communicate.
    Through the use of computational techniques, visualization helps researchers explore datasets, identify hidden patterns, and gain insights that would otherwise remain obscure in numerical form.
    """
)

banner_image = 'https://raw.githubusercontent.com/fakhitah3/FHPK-TVET/main/3u1i_2.jpeg'
st.image(banner_image, use_container_width=True)

# Add the extended explanation
st.write(
    """
    The aim of scientific visualization is not merely to present data attractively, but to **enhance comprehension and decision-making** through visual analytics.
    Applications span across disciplines such as **climate science**, **medicine**, **engineering**, **data science**, and **environmental studies**.

    In this course or module, students will learn to:
    - Select relevant datasets for analysis and visualization.
    - Apply various visualization techniques such as graphs, maps, and 3D models.
    - Interpret visual outputs to support scientific conclusions and policy recommendations.
   
    By the end of this exercise, students should be able to produce **informative, accurate, and interactive visualizations** that effectively communicate scientific findings to both expert and non-expert audiences.
    """
)
