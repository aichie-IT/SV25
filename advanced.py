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
    with st.expander("Filter Options", expanded=True):
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
theme_mode = st.sidebar.radio("Select Theme Mode", ["Light", "Dark"], horizontal=True)

if theme_mode == "Dark":
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

st.subheader("Advanced Statistical Visualizations")
st.markdown("Explore deeper numerical relationships using box, violin, and scatter plots.")

# Summary box
corr_pair = df.corr(numeric_only=True).abs().unstack().sort_values(ascending=False)
top_corr = corr_pair[corr_pair < 1].head(1)
feature_a, feature_b = top_corr.index[0]
value = top_corr.values[0]
st.metric("Strongest Correlation", f"{feature_a} ↔ {feature_b}", f"{value:.2f}", border=True)

st.markdown("### Summary")
st.info("""
These visualizations explore how accident severity interacts with continuous variables like age, 
speed, and distance. Box and violin plots show clear separation in speed and experience across 
severity levels. Scatter plots reveal positive relationships between higher bike speed and greater 
accident severity, confirming that speed remains a dominant factor.
""")
st.markdown("---")
    
sns.set_style("whitegrid")

# Helper function
def show_plot(title, xlabel, ylabel, rotation=False):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if rotation:
        plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()

# --- BOX PLOTS ---
with st.expander("Box Plots"):
    plt.figure(figsize=(12, 7))
    sns.boxplot(x='Accident_Severity', y='Biker_Age', data=filtered_df, palette='viridis')
    show_plot('Distribution of Biker Age by Accident Severity', 'Accident Severity', 'Biker Age')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    plt.figure(figsize=(12, 7))
    sns.boxplot(x='Accident_Severity', y='Riding_Experience', data=filtered_df, palette='viridis')
    show_plot('Distribution of Riding Experience by Accident Severity', 'Accident Severity', 'Riding Experience (Years)')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    plt.figure(figsize=(12, 7))
    sns.boxplot(x='Accident_Severity', y='Daily_Travel_Distance', data=filtered_df, palette='viridis')
    show_plot('Distribution of Daily Travel Distance by Accident Severity', 'Accident Severity', 'Daily Travel Distance')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    plt.figure(figsize=(12, 7))
    sns.boxplot(x='Accident_Severity', y='Bike_Speed', data=filtered_df, palette='viridis')
    show_plot('Distribution of Bike Speed by Accident Severity', 'Accident Severity', 'Bike Speed')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    plt.figure(figsize=(12, 7))
    sns.boxplot(x='Accident_Severity', y='Speed_Limit', data=filtered_df, palette='viridis')
    show_plot('Distribution of Speed Limit by Accident Severity', 'Accident Severity', 'Speed Limit')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    plt.figure(figsize=(12, 7))
    sns.boxplot(x='Biker_Occupation', y='Bike_Speed', data=filtered_df, palette='viridis')
    show_plot('Distribution of Bike Speed by Biker Occupation', 'Biker Occupation', 'Bike Speed', rotation=True)
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

# --- VIOLIN PLOTS ---
with st.expander("Violin Plots"):
    plt.figure(figsize=(12, 7))
    sns.violinplot(x='Accident_Severity', y='Biker_Age', data=filtered_df, palette='viridis')
    show_plot('Distribution of Biker Age by Accident Severity (Violin Plot)', 'Accident Severity', 'Biker Age')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    plt.figure(figsize=(12, 7))
    sns.violinplot(x='Weather', y='Bike_Speed', data=filtered_df, palette='viridis')
    show_plot('Distribution of Bike Speed by Weather (Violin Plot)', 'Weather', 'Bike Speed')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

# --- SCATTER PLOTS ---
with st.expander("Scatter Plots"):
    plt.figure(figsize=(14, 10))
    sns.scatterplot(x='Bike_Speed', y='Daily_Travel_Distance', hue='Accident_Severity', data=filtered_df, palette='viridis', alpha=0.6)
    plt.legend(title='Accident Severity')
    show_plot('Daily Travel Distance vs Bike Speed by Accident Severity', 'Bike Speed', 'Daily Travel Distance')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='Bike_Speed', y='Biker_Age', data=filtered_df, alpha=0.6)
    show_plot('Biker Age vs Bike Speed', 'Bike Speed', 'Biker Age')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='Daily_Travel_Distance', y='Biker_Age', data=filtered_df, alpha=0.6)
    show_plot('Biker Age vs Daily Travel Distance', 'Daily Travel Distance', 'Biker Age')
    st.success("**Interpretation:** Younger bikers show higher accident severity, suggesting overconfidence and less risk awareness.")

st.markdown("#### 💬 Observation")
st.success("""
The violin plots highlight that severe accidents are concentrated among high-speed riders. 
Correlations between experience and severity indicate that experienced riders adapt speed 
better to conditions, validating behavioral safety theories.
""")

