import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
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

# --- MAIN TITLE ---
st.title("🏍️ Motorbike Accident Insights Dashboard")
st.markdown("Explore accident patterns and biker behaviors with interactive visual analytics.")

st.markdown("---")

# --- SUMMARY BOX ---
col1, col2, col3, col4 = st.columns(4)

if not filtered_df.empty:
    col1.metric("Total Records", f"{len(filtered_df):,}", help="PLO 1: Total Motor Accident Records", border=True)
    col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f} years", help="PLO 2: Average Biker Age", border=True)
    col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h", help="PLO 3: Average Bike Speed", border=True)
    col4.metric("Avg. Travel Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km", help="PLO 4: Average Daily Travel Distance", border=True)
else:
    col1.metric("Total Records", "0", help="No data available")
    col2.metric("Avg. Age", "N/A", help="No data available")
    col3.metric("Avg. Speed", "N/A", help="No data available")
    col4.metric("Avg. Travel Distance", "N/A", help="No data available")

st.markdown("---")

# --- TAB LAYOUT ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "⚙️ General Overview", 
    "📊 Accident Factors", 
    "📈 Numerical Analysis", 
    "📉 Advanced Visualizations", 
    "📈 Correlation Insights", 
    "🏍️ Riding Behavior Insights"
])

# ============ TAB 1: GENERAL OVERVIEW ============
with tab1:
    st.subheader("Distribution Overview")
    st.markdown("Overview of accident severity, helmet use, and license validity.")

    # Summary box
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{len(filtered_df):,}")
    col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f}")
    col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h")
    col4.metric("Helmet Usage (%)", f"{(filtered_df['Wearing_Helmet'].value_counts(normalize=True).get('Yes',0)*100):.1f}%")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        fig1 = px.pie(filtered_df, names="Accident_Severity", title="Accident Severity", color_discrete_sequence=color_theme)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.pie(filtered_df, names="Wearing_Helmet", title="Wearing Helmet", color_discrete_sequence=color_theme)
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        fig3 = px.pie(filtered_df, names="Valid_Driving_License", title="Valid License", color_discrete_sequence=color_theme)
        st.plotly_chart(fig3, use_container_width=True)


# ============ TAB 2: ACCIDENT FACTORS ============
with tab2:
    st.subheader("Accident Severity by Contributing Factors")
    st.markdown("Explore how factors like occupation, education, and road conditions impact severity.")

    # Summary
    col1, col2, col3 = st.columns(3)
    top_severity = filtered_df['Accident_Severity'].mode()[0]
    top_weather = filtered_df['Weather'].mode()[0]
    top_road = filtered_df['Road_Type'].mode()[0]
    col1.metric("Most Common Severity", top_severity)
    col2.metric("Common Weather", top_weather)
    col3.metric("Frequent Road Type", top_road)

    st.markdown("---")

    # Charts
    categorical_cols = ["Biker_Occupation", "Biker_Education_Level", "Weather", "Road_Type", "Traffic_Density", "Biker_Alcohol"]
    for col in categorical_cols:
        agg_df = filtered_df.groupby([col, "Accident_Severity"]).size().reset_index(name="Count")
        fig = px.bar(agg_df, x=col, y="Count", color="Accident_Severity", barmode="group", 
                     color_discrete_sequence=color_theme, title=f"Accident Severity by {col.replace('_', ' ')}")
        st.plotly_chart(fig, use_container_width=True)


# ============ TAB 3: NUMERICAL ANALYSIS ============
with tab3:
    st.subheader("Numeric Data Distributions")

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg. Bike Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h")
    col2.metric("Avg. Daily Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km")
    col3.metric("Avg. Riding Experience", f"{filtered_df['Riding_Experience'].mean():.1f} years")

    st.markdown("---")

    numeric_cols = ["Biker_Age", "Bike_Speed", "Daily_Travel_Distance", "Riding_Experience"]
    for col in numeric_cols:
        fig = px.histogram(filtered_df, x=col, nbins=20, color_discrete_sequence=color_theme, title=f"Distribution of {col.replace('_',' ')}")
        st.plotly_chart(fig, use_container_width=True)


# ============ TAB 4: ADVANCED VISUALIZATIONS ============
with tab4:
    st.subheader("Statistical & Comparative Visuals")
    st.markdown("Deeper exploration using box and scatter plots.")

    # Summary
    corr_pair = df.corr(numeric_only=True).abs().unstack().sort_values(ascending=False)
    top_corr = corr_pair[corr_pair < 1].head(1)
    feature_a, feature_b = top_corr.index[0]
    value = top_corr.values[0]
    st.metric("Strongest Correlation", f"{feature_a} ↔ {feature_b}", f"{value:.2f}")

    st.markdown("---")

    # Example visual
    fig = px.box(filtered_df, x="Accident_Severity", y="Bike_Speed", color="Accident_Severity",
                 title="Bike Speed by Accident Severity", color_discrete_sequence=color_theme)
    st.plotly_chart(fig, use_container_width=True)


# ============ TAB 5: CORRELATION INSIGHTS ============
with tab5:
    st.subheader("Feature Correlation Matrix")
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns
    corr = df[numeric_cols].corr()

    col1, col2 = st.columns(2)
    top_corr = corr.unstack().sort_values(ascending=False)
    col1.metric("Highest Positive Correlation", top_corr.index[1][0], f"{top_corr.iloc[1]:.2f}")
    col2.metric("Lowest Negative Correlation", top_corr.index[-1][0], f"{top_corr.iloc[-1]:.2f}")

    fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap", aspect="auto", color_continuous_scale="Tealrose")
    st.plotly_chart(fig, use_container_width=True)


# ============ TAB 6: RIDING BEHAVIOR INSIGHTS ============
with tab6:
    st.subheader("Rider Behavior Patterns")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Helmet Usage", f"{(filtered_df['Wearing_Helmet'].value_counts(normalize=True).get('Yes',0)*100):.1f}%")
    col2.metric("Alcohol Usage", f"{(filtered_df['Biker_Alcohol'].value_counts(normalize=True).get('Yes',0)*100):.1f}%")
    col3.metric("Talk While Riding", f"{(filtered_df['Talk_While_Riding'].value_counts(normalize=True).get('Yes',0)*100):.1f}%")
    col4.metric("Smoke While Riding", f"{(filtered_df['Smoke_While_Riding'].value_counts(normalize=True).get('Yes',0)*100):.1f}%")

    st.markdown("---")

    for col in ["Talk_While_Riding", "Smoke_While_Riding", "Wearing_Helmet", "Biker_Alcohol"]:
        if col in filtered_df.columns:
            data = filtered_df[col].value_counts().reset_index()
            data.columns = [col, "Count"]
            fig = px.bar(data, x=col, y="Count", text="Count", color=col,
                         color_discrete_sequence=color_theme, title=f"{col.replace('_',' ')} Distribution")
            fig.update_traces(textposition="outside")
            fig.update_layout(showlegend=False, title_x=0.5, yaxis_title="Count", margin=dict(t=60, b=40))
            st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Motorbike Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
