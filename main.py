import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Motorbike Accident Insights Dashboard", page_icon="🏍️", layout="wide")

# ===== THEME TOGGLE =====
st.sidebar.markdown("### 🌓 Theme Settings")
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

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/motor_accident.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# ====== SIDEBAR ======
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/743/743922.png", width=80)
    st.title("⚙️ Dashboard Controls")
    st.markdown("### 🧾 Data Summary")
    st.info(f"**Total Records:** {len(df):,}\n\n**Columns:** {len(df.columns)}")

    # --- Multiselect Filters ---
    st.markdown("🎯 Filter Options")
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

    # Optional Filters
    alcohol = st.multiselect(
        "Biker Alcohol Consumption",
        options=sorted(df["Biker_Alcohol"].dropna().unique()) if "Biker_Alcohol" in df.columns else [],
        default=sorted(df["Biker_Alcohol"].dropna().unique()) if "Biker_Alcohol" in df.columns else []
    )
    traffic = st.multiselect(
        "Traffic Density",
        options=sorted(df["Traffic_Density"].dropna().unique()) if "Traffic_Density" in df.columns else [],
        default=sorted(df["Traffic_Density"].dropna().unique()) if "Traffic_Density" in df.columns else []
    )
    license_status = st.multiselect(
        "Valid Driving License",
        options=sorted(df["Valid_Driving_License"].dropna().unique()) if "Valid_Driving_License" in df.columns else [],
        default=sorted(df["Valid_Driving_License"].dropna().unique()) if "Valid_Driving_License" in df.columns else []
    )

    # Numeric Filter
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
    filtered_df = df[
        df["Accident_Severity"].isin(severity) &
        df["Weather"].isin(weather) &
        df["Time_of_Day"].isin(time_of_day) &
        df["Road_Type"].isin(road_type)
    ]
    if alcohol: filtered_df = filtered_df[filtered_df["Biker_Alcohol"].isin(alcohol)]
    if traffic: filtered_df = filtered_df[filtered_df["Traffic_Density"].isin(traffic)]
    if license_status: filtered_df = filtered_df[filtered_df["Valid_Driving_License"].isin(license_status)]
    if min_age is not None: filtered_df = filtered_df[
        (filtered_df["Biker_Age"] >= min_age) & (filtered_df["Biker_Age"] <= max_age)
    ]

    # --- Reset & Download ---
    st.markdown("---")
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
    st.caption("Designed with ❤️ using Streamlit")

# --- MAIN TITLE ---
st.title("🏍️ Motorbike Accident Insights Dashboard")
st.markdown("Explore accident patterns and biker behaviors with interactive visual analytics.")
st.markdown("---")

# --- SUMMARY CARDS ---
col1, col2, col3, col4 = st.columns(4)
if not filtered_df.empty:
    col1.metric("Total Records", f"{len(filtered_df):,}")
    col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f} years")
    col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h")
    col4.metric("Avg. Travel Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km")
else:
    col1.metric("Total Records", "0")
    col2.metric("Avg. Age", "N/A")
    col3.metric("Avg. Speed", "N/A")
    col4.metric("Avg. Travel Distance", "N/A")

st.markdown("---")

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚙️ General Overview", "📊 Accident Factors", 
    "📈 Numerical Analysis", "📉 Advanced Visualizations", "🗺️ Geographical Distribution"
])

# ============ TAB 1: GENERAL OVERVIEW ============
with tab1:
    st.subheader("Distribution Overview")
    if not filtered_df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            fig = px.pie(filtered_df, names="Accident_Severity", title="Accident Severity Distribution", color_discrete_sequence=color_theme)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(filtered_df, names="Wearing_Helmet", title="Wearing Helmet Distribution", color_discrete_sequence=color_theme)
            st.plotly_chart(fig, use_container_width=True)
        with col3:
            fig = px.pie(filtered_df, names="Valid_Driving_License", title="Valid Driving License Distribution", color_discrete_sequence=color_theme)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# ============ TAB 2: ACCIDENT FACTORS ============
with tab2:
    st.subheader("Accident Severity by Categorical Factors")
    if not filtered_df.empty:
        # Occupation
        agg_occ = filtered_df.groupby(["Biker_Occupation","Accident_Severity"]).size().reset_index(name="Count")
        fig = px.bar(agg_occ, x="Biker_Occupation", y="Count", color="Accident_Severity", barmode="group", color_discrete_sequence=color_theme, title="Accident Severity by Biker Occupation")
        st.plotly_chart(fig, use_container_width=True)

        # Education
        agg_edu = filtered_df.groupby(["Biker_Education_Level","Accident_Severity"]).size().reset_index(name="Count")
        fig = px.bar(agg_edu, x="Biker_Education_Level", y="Count", color="Accident_Severity", barmode="group", color_discrete_sequence=color_theme, title="Accident Severity by Biker Education Level")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# ============ TAB 3: NUMERICAL ANALYSIS ============
with tab3:
    st.subheader("Distribution of Numeric Variables")
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(px.histogram(filtered_df, x="Biker_Age", nbins=20, color_discrete_sequence=color_theme), use_container_width=True)
            st.plotly_chart(px.histogram(filtered_df, x="Bike_Speed", nbins=20, color_discrete_sequence=color_theme), use_container_width=True)
        with col2:
            st.plotly_chart(px.histogram(filtered_df, x="Riding_Experience", nbins=20, color_discrete_sequence=color_theme), use_container_width=True)
            st.plotly_chart(px.histogram(filtered_df, x="Daily_Travel_Distance", nbins=20, color_discrete_sequence=color_theme), use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# ============ TAB 4: ADVANCED VISUALIZATIONS ============
with tab4:
    st.subheader("Advanced Statistical Visualizations")
    if not filtered_df.empty:
        sns.set_style("whitegrid")
        def show_plot(title, xlabel, ylabel, rotation=False):
            plt.title(title); plt.xlabel(xlabel); plt.ylabel(ylabel)
            if rotation: plt.xticks(rotation=45, ha='right')
            plt.tight_layout(); st.pyplot(plt.gcf()); plt.clf()

        # Box plot example
        plt.figure(figsize=(12,7))
        sns.boxplot(x='Accident_Severity', y='Biker_Age', data=filtered_df, palette='viridis')
        show_plot('Distribution of Biker Age by Accident Severity', 'Accident Severity', 'Biker Age')
    else:
        st.warning("No data available for the selected filters.")

# ============ TAB 5: MAP ============
with tab5:
    st.subheader("🗺️ Geographical Distribution")
    if not filtered_df.empty and "Latitude" in filtered_df.columns and "Longitude" in filtered_df.columns:
        st.map(filtered_df[["Latitude","Longitude"]])
    else:
        st.warning("Map data not available for the selected filters.")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Motorbike Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
