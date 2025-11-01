import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Motorbike Accident Insights Dashboard", page_icon="🏍️", layout="wide")


# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/motor_accident.csv"
    df = pd.read_csv(url)
    return df

df = load_data()


# ====== SIDEBAR ======
with st.sidebar:
    st.title("Dashboard Controls")

    # --- Data Summary ---
    st.markdown("### 🧾 Data Summary")
    st.info(f"**Total Records:** {len(df):,}\n\n**Columns:** {len(df.columns)}")

    # --- Filters Section ---
    with st.expander("🎯 Filter Options", expanded=True):
        st.markdown("Select filters to refine your dashboard view:")

        # --- Multi-select Filters ---
        severity = st.multiselect(
            "Accident Severity",
            options=sorted(df["Accident_Severity"].dropna().unique()),
            default=sorted(df["Accident_Severity"].dropna().unique())
        )

        weather = st.multiselect(
            "Weather Condition",
            options=sorted(df["Weather"].dropna().unique()),
            default=sorted(df["Weather"].dropna().unique())
        )

        time_of_day = st.multiselect(
            "Time of Day",
            options=sorted(df["Time_of_Day"].dropna().unique()),
            default=sorted(df["Time_of_Day"].dropna().unique())
        )

        road_type = st.multiselect(
            "Road Type",
            options=sorted(df["Road_Type"].dropna().unique()),
            default=sorted(df["Road_Type"].dropna().unique())
        )

        # --- Optional Filters ---
        if "Biker_Alcohol" in df.columns:
            alcohol = st.multiselect(
                "Biker Alcohol Consumption",
                options=sorted(df["Biker_Alcohol"].dropna().unique()),
                default=sorted(df["Biker_Alcohol"].dropna().unique())
            )
        else:
            alcohol = []

        if "Traffic_Density" in df.columns:
            traffic = st.multiselect(
                "Traffic Density",
                options=sorted(df["Traffic_Density"].dropna().unique()),
                default=sorted(df["Traffic_Density"].dropna().unique())
            )
        else:
            traffic = []

        if "Valid_Driving_License" in df.columns:
            license_status = st.multiselect(
                "Valid Driving License",
                options=sorted(df["Valid_Driving_License"].dropna().unique()),
                default=sorted(df["Valid_Driving_License"].dropna().unique())
            )
        else:
            license_status = []

        # --- Numeric Filter: Biker Age ---
        if "Biker_Age" in df.columns:
            min_age, max_age = st.slider(
                "Filter by Biker Age",
                int(df["Biker_Age"].min()),
                int(df["Biker_Age"].max()),
                (int(df["Biker_Age"].min()), int(df["Biker_Age"].max()))
            )
        else:
            min_age, max_age = None, None

        # --- Apply Filters ---
        filtered_df = df.copy()

        if severity:
            filtered_df = filtered_df[filtered_df["Accident_Severity"].isin(severity)]
        if weather:
            filtered_df = filtered_df[filtered_df["Weather"].isin(weather)]
        if time_of_day:
            filtered_df = filtered_df[filtered_df["Time_of_Day"].isin(time_of_day)]
        if road_type:
            filtered_df = filtered_df[filtered_df["Road_Type"].isin(road_type)]
        if alcohol:
            filtered_df = filtered_df[filtered_df["Biker_Alcohol"].isin(alcohol)]
        if traffic:
            filtered_df = filtered_df[filtered_df["Traffic_Density"].isin(traffic)]
        if license_status:
            filtered_df = filtered_df[filtered_df["Valid_Driving_License"].isin(license_status)]
        if min_age is not None:
            filtered_df = filtered_df[
                (filtered_df["Biker_Age"] >= min_age) & (filtered_df["Biker_Age"] <= max_age)
            ]

    # --- Reset and Download Buttons ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset Filters"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    with col2:
        st.download_button(
            label="Download CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="motor_accident_data.csv",
            mime="text/csv"
        )
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

st.subheader("Distribution of Numeric Variables")
st.markdown("Analyze numeric relationships such as speed, age, experience, and travel distance.")

col1, col2, col3 = st.columns(3)
col1.metric("Avg. Bike Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h", border=True)
col2.metric("Avg. Daily Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km", border=True)
col3.metric("Avg. Riding Experience", f"{filtered_df['Riding_Experience'].mean():.1f} years", border=True)

st.markdown("### Summary")
st.info("""
Numerical distributions reveal that most bikers are within the mid-age range with moderate experience. 
Speed and daily distance vary widely, reflecting diverse riding habits. The data indicates that 
excessive speed is a major contributor to higher accident severity, whereas more riding experience 
correlates with fewer severe outcomes.
""")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    fig6 = px.histogram(
        filtered_df, x="Biker_Age", nbins=20,
        title="Distribution of Biker Age",
        color_discrete_sequence=color_theme
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.success("""
    **Interpretation:** Most bikers are aged between 20–40, which corresponds to moderate accident severity, possibly due to higher riding activity.
    """)

    fig7 = px.histogram(
        filtered_df, x="Bike_Speed", nbins=20,
        title="Distribution of Bike Speed",
        color_discrete_sequence=color_theme
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.warning("""
    **Interpretation:** Speed distribution skews toward 60–80 km/h, and riders above this range tend to experience more severe accidents.
    """)

with col2:
    fig8 = px.histogram(
        filtered_df, x="Riding_Experience", nbins=20,
        title="Distribution of Riding Experience",
        color_discrete_sequence=color_theme
    )
    st.plotly_chart(fig8, use_container_width=True)
    st.info("""
    **Interpretation:** Greater riding experience is associated with fewer accidents, highlighting the protective role of skill and familiarity.
    """)

    fig9 = px.histogram(
        filtered_df, x="Daily_Travel_Distance", nbins=20,
        title="Distribution of Daily Travel Distance",
        color_discrete_sequence=color_theme
    )
    st.plotly_chart(fig9, use_container_width=True)
    st.success("""
    **Interpretation:** Moderate daily travel distances (10–30 km) dominate the dataset, while excessive distance relates to fatigue and higher risk.
    """)
st.markdown("#### 💬 Observation")
st.success("""
Riders with greater experience tend to maintain safer speeds. The histogram peaks for moderate 
speed and mid-age groups align with less severe accident rates, reinforcing the role of skill 
and maturity in risk mitigation.
""")
