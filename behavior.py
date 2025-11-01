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

st.subheader("Riding Behavior Insights")
st.markdown("Analyze rider behavior patterns and how habits influence accident severity.")

# Calculate percentages
helmet = (filtered_df['Wearing_Helmet'].value_counts(normalize=True).get('Yes', 0) * 100)
alcohol = (filtered_df['Biker_Alcohol'].value_counts(normalize=True).get('Yes', 0) * 100)
talk = (filtered_df['Talk_While_Riding'].value_counts(normalize=True).get('Yes', 0) * 100)
smoke = (filtered_df['Smoke_While_Riding'].value_counts(normalize=True).get('Yes', 0) * 100)

# Styled metric summary using HTML/CSS
st.markdown("""
<style>
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        flex: 1;
        background: #f9f9f9;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: bold;
    }
    .good { color: #2e7d32; }      /* Green for positive behavior */
    .warning { color: #f57c00; }   /* Orange for risk behaviors */
    .bad { color: #c62828; }       /* Red for negative behaviors */
</style>
""", unsafe_allow_html=True)

# Display metric boxes
st.markdown(f"""
<div class="metric-container">
    <div class="metric-card">
        <div class="metric-title">Helmet Usage</div>
        <div class="metric-value {'good' if helmet > 70 else 'warning'}">{helmet:.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Alcohol Usage</div>
        <div class="metric-value {'bad' if alcohol > 10 else 'good'}">{alcohol:.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Talk While Riding</div>
        <div class="metric-value {'bad' if talk > 20 else 'good'}">{talk:.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Smoke While Riding</div>
        <div class="metric-value {'bad' if smoke > 20 else 'good'}">{smoke:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Summary")
st.info("""
Behavior-based insights demonstrate how individual actions contribute to safety outcomes. 
Helmet usage is high but inconsistent across demographics, while alcohol and distraction behaviors 
(talking or smoking) remain significant risk enhancers. These findings reinforce behavioral safety 
as a cornerstone of accident prevention.
""")
st.markdown("---")

# Define behavior columns and color palette
behavior_cols = ["Talk_While_Riding", "Smoke_While_Riding", "Wearing_Helmet", "Biker_Alcohol"]
color_theme = px.colors.qualitative.Pastel

# Professional bar charts
for col in behavior_cols:
    if col in filtered_df.columns:
        data = filtered_df[col].value_counts().reset_index()
        data.columns = [col, "Count"]

        fig = px.bar(
            data,
            x=col,
            y="Count",
            text="Count",
            color=col,
            color_discrete_sequence=color_theme,
            title=f"{col.replace('_', ' ')} Distribution"
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Count",
            title_x=0.0,
            title_y=0.95,
            title_font=dict(size=16, family="Arial", color="black"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=40),
        )

        st.plotly_chart(fig, use_container_width=True)
        st.success(f"""
        **Interpretation:** The {col.replace('_',' ').lower()} pattern reveals behavioral influence on safety outcomes.
        Higher counts in risky behaviors (e.g., alcohol or distraction) align with increased accident rates.
        """)

st.markdown("#### 💬 Observation")
st.success("""
Riders who talk or smoke while riding show higher accident frequencies, validating the role of 
attention in safety. Helmet use correlates inversely with severe accidents, supporting mandatory 
safety gear enforcement.
""")
