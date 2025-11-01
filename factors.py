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
    st.markdown(
    """
    <style>
    /* Card-like filter boxes */
    .stMultiSelect, .stSlider {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 8px 10px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    /* Selected filter tags */
    div[data-baseweb="tag"] {
        background-color: #6c757d !important; /* gray tone */
        color: white !important;
        border-radius: 6px !important;
    }

    /* Close (x) button inside tags */
    div[data-baseweb="tag"] svg {
        fill: white !important;
    }

    /* Slider color styling */
    .stSlider > div > div > div[data-testid="stThumbValue"] {
        color: #0073e6 !important;
        font-weight: bold !important;
    }
    .stSlider > div > div > div[data-testid="stTickBar"] {
        background: linear-gradient(to right, #0073e6, #00b894) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

        
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

st.subheader("Accident Severity by Categorical Factors")
st.markdown("Explore how factors like occupation, education, and road conditions impact severity.")

# ===== COLOR & ORDER SETTINGS =====
severity_order = ["No Accident", "Moderate Accident", "Severe Accident"]
severity_colors = {
    "No Accident": "#A8E6CF",       # Pastel Green
    "Moderate Accident": "#FFF3B0", # Pastel Yellow
    "Severe Accident": "#FFD3B6"    # Pastel Orange
}

# Force correct dtype & order for Accident_Severity
filtered_df["Accident_Severity"] = pd.Categorical(
    filtered_df["Accident_Severity"], categories=severity_order, ordered=True
)
    
# Summary
col1, col2, col3 = st.columns(3)
top_severity = filtered_df['Accident_Severity'].mode()[0]
top_weather = filtered_df['Weather'].mode()[0]
top_road = filtered_df['Road_Type'].mode()[0]
col1.metric("Most Common Severity", top_severity, border=True)
col2.metric("Common Weather", top_weather, border=True)
col3.metric("Frequent Road Type", top_road, border=True)

st.markdown("### Summary")
st.info("""
Accident patterns vary significantly across occupational, educational, and environmental factors. 
Riders from certain occupations or lower education levels tend to experience more severe accidents, 
possibly due to riskier job exposure or lower safety awareness. Road and weather conditions also 
strongly influence accident frequency, especially on wet or uneven surfaces. Understanding these 
categorical trends allows targeted interventions to improve safety.
""")
st.markdown("---")

# --- OCCUPATION ---
agg_occ = (
    filtered_df.groupby(["Biker_Occupation", "Accident_Severity"])
    .size()
    .reset_index(name="Count")
)
fig4 = px.bar(
    agg_occ,
    x="Biker_Occupation",
    y="Count",
    color="Accident_Severity",
    title="Accident Severity by Biker Occupation",
    color_discrete_sequence=color_theme,
    barmode="group"
)

# --- EDUCATION ---
agg_edu = (
    filtered_df.groupby(["Biker_Education_Level", "Accident_Severity"])
    .size()
    .reset_index(name="Count")
)
fig5 = px.bar(
    agg_edu,
    x="Biker_Education_Level",
    y="Count",
    color="Accident_Severity",
    title="Accident Severity by Biker Education Level",
    color_discrete_sequence=color_theme,
    barmode="group"
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig4, use_container_width=True)
    st.info("""
    *Interpretation:* Riders in delivery or transport occupations report higher accident severity, likely due to increased road exposure.
    """)
with col2:
    st.plotly_chart(fig5, use_container_width=True)
    st.info("""
    *Interpretation:* Bikers with higher education levels show lower accident severity, reflecting better safety awareness and risk management.
    """)

st.markdown("---")
st.subheader("Other Influencing Factors")

# --- LOOP FOR OTHER CATEGORICAL VARIABLES ---
categorical_cols = [
    "Wearing_Helmet", "Motorcycle_Ownership", "Valid_Driving_License",
    "Bike_Condition", "Road_Type", "Road_condition", "Weather",
    "Time_of_Day", "Traffic_Density", "Biker_Alcohol"
]

# Consistent color mapping
severity_colors_map = {
"No Accident": "#A8E6CF",       # Pastel Green
"Moderate Accident": "#FFF3B0", # Pastel Yellow
"Severe Accident": "#FFD3B6"    # Pastel Orange
}

# Ensure categorical order for plotting
filtered_df["Accident_Severity"] = pd.Categorical(
filtered_df["Accident_Severity"], categories=severity_order, ordered=True
)

# Display 2 charts per row
for i in range(0, len(categorical_cols), 2):
    col1, col2 = st.columns(2)

    for j, col in enumerate(categorical_cols[i:i+2]):
            
        agg_df = (
            filtered_df.groupby([col, "Accident_Severity"])
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )

        fig = px.bar(
            agg_df,
            x=col,
            y="Count",
            color="Accident_Severity",
            title=f"Accident Severity by {col.replace('_', ' ')}",
            color_discrete_map=severity_colors_map,
            category_orders={"Accident_Severity": severity_order},
            barmode="group"
        )

        # Force bars to use fully solid fill (no shading or transparency)
        fig.for_each_trace(lambda t: t.update(marker=dict(line=dict(width=0), opacity=1.0)))

        # Remove the default Plotly gradient shading
        fig.update_traces(marker_coloraxis=None)

        # Force consistent flat color rendering
        fig.update_layout(
            template=None,  # remove plotly's default style template
            plot_bgcolor="white",
            paper_bgcolor="white",
            bargap=0.25,
        )

        if j == 0:
            with col1:
                st.plotly_chart(fig, use_container_width=True)
                st.info(f"""*Interpretation:* The chart shows how {col.replace('_',' ').lower()} affects accident severity, where imbalance across categories indicates risk-prone conditions.""")
        else:
            with col2:
                st.plotly_chart(fig, use_container_width=True)
                st.info(f"""*Interpretation:* The chart shows how {col.replace('_',' ').lower()} affects accident severity, where imbalance across categories indicates risk-prone conditions.""")


st.markdown("#### 💬 Observation")
st.success("""
The grouped bar charts reveal that higher education correlates with fewer severe accidents, 
while adverse weather and poor road types contribute to higher accident counts. 
These findings support public safety campaigns focusing on awareness and road infrastructure improvements.
""")

