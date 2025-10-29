import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title="Road Accident Insights Dashboard",
    page_icon="🚗",
    layout="wide"
)

# ====== COLOR THEME ======
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

    # --- Summary box ---
    st.markdown("### 🧾 Data Summary")
    st.info(f"**Total Records:** {len(df):,}\n\n**Columns:** {len(df.columns)}")

    # --- Filters section ---
    with st.expander("🎯 Filter Options", expanded=True):
        st.markdown("Select filters to refine your dashboard view:")

        # Dropdown filters
        severity = st.selectbox(
            "Select Accident Severity",
            ["All"] + sorted(df["Accident_Severity"].dropna().unique().tolist())
        )

        weather = st.selectbox(
            "Select Weather Condition",
            ["All"] + sorted(df["Weather"].dropna().unique().tolist())
        )

        time_of_day = st.selectbox(
            "Select Time of Day",
            ["All"] + sorted(df["Time_of_Day"].dropna().unique().tolist())
        )

        road_type = st.selectbox(
            "Select Road Type",
            ["All"] + sorted(df["Road_Type"].dropna().unique().tolist())
        )

        # Numeric filter
        if "Biker_Age" in df.columns:
            min_age, max_age = st.slider(
                "Filter by Biker Age",
                int(df["Biker_Age"].min()),
                int(df["Biker_Age"].max()),
                (int(df["Biker_Age"].min()), int(df["Biker_Age"].max()))
            )
        else:
            min_age, max_age = None, None

        # Apply filters
        filtered_df = df.copy()
        if severity != "All":
            filtered_df = filtered_df[filtered_df["Accident_Severity"] == severity]
        if weather != "All":
            filtered_df = filtered_df[filtered_df["Weather"] == weather]
        if time_of_day != "All":
            filtered_df = filtered_df[filtered_df["Time_of_Day"] == time_of_day]
        if road_type != "All":
            filtered_df = filtered_df[filtered_df["Road_Type"] == road_type]
        if min_age is not None:
            filtered_df = filtered_df[
                (filtered_df["Biker_Age"] >= min_age) & (filtered_df["Biker_Age"] <= max_age)
            ]

    # --- Reset button ---
    if st.button("🔄 Reset Filters"):
        st.experimental_rerun()

    st.markdown("---")
    st.caption("Designed with ❤️ using Streamlit")

# ====== MAIN PAGE ======
st.title("🚗 Road Accident Insights Dashboard")
st.markdown("Explore accident patterns, biker demographics, and contributing factors using interactive visuals.")

st.markdown("---")

# ====== SUMMARY METRICS ======
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", f"{len(filtered_df):,}", help="Total number of accident records", border=True)
col2.metric("Avg. Biker Age", f"{filtered_df['Biker_Age'].mean():.1f} years", help="Average biker age", border=True)
col3.metric("Avg. Bike Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h", help="Average motorcycle speed", border=True)
col4.metric("Avg. Travel Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km", help="Average daily distance", border=True)

st.markdown("---")

# ====== TABS ======
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 General Overview",
    "🏍️ Accident Factors",
    "🔢 Numerical Analysis",
    "📈 Advanced Visualizations"
])

# ============ TAB 1: GENERAL OVERVIEW ============
with tab1:
    st.subheader("📊 Overview of Accident Distributions")
    col1, col2, col3 = st.columns(3)

    # Pie: Accident Severity
    with col1:
        fig1 = px.pie(
            filtered_df,
            names="Accident_Severity",
            title="Accident Severity Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Pie: Helmet Usage
    with col2:
        fig2 = px.pie(
            filtered_df,
            names="Wearing_Helmet",
            title="Helmet Usage Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Pie: Valid License
    with col3:
        fig3 = px.pie(
            filtered_df,
            names="Valid_Driving_License",
            title="Valid License Ownership",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig3, use_container_width=True)

# ============ TAB 2: ACCIDENT FACTORS ============
with tab2:
    st.subheader("🏍️ Accident Severity by Categorical Factors")

    categorical_cols = [
        "Biker_Occupation", "Biker_Education_Level",
        "Wearing_Helmet", "Motorcycle_Ownership", "Valid_Driving_License",
        "Bike_Condition", "Road_Type", "Road_condition",
        "Weather", "Time_of_Day", "Traffic_Density", "Biker_Alcohol"
    ]

    for col in categorical_cols:
        if col in filtered_df.columns:
            fig = px.bar(
                filtered_df,
                y=col,
                color="Accident_Severity",
                title=f"Accident Severity by {col.replace('_', ' ')}",
                color_discrete_sequence=color_theme
            )
            st.plotly_chart(fig, use_container_width=True)

# ============ TAB 3: NUMERICAL ANALYSIS ============
with tab3:
    st.subheader("🔢 Numerical Variables Distribution")

    num_cols = ["Biker_Age", "Bike_Speed", "Riding_Experience", "Daily_Travel_Distance"]
    num_cols = [col for col in num_cols if col in filtered_df.columns]

    col1, col2 = st.columns(2)
    for i, col in enumerate(num_cols):
        fig = px.histogram(
            filtered_df, x=col, nbins=20,
            title=f"Distribution of {col.replace('_', ' ')}",
            color_discrete_sequence=color_theme
        )
        if i % 2 == 0:
            with col1: st.plotly_chart(fig, use_container_width=True)
        else:
            with col2: st.plotly_chart(fig, use_container_width=True)

# ============ TAB 4: ADVANCED VISUALIZATIONS ============
with tab4:
    st.subheader("📈 Advanced Relationship Visualizations")
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
    with st.expander("📦 Box Plots"):
        if "Biker_Age" in filtered_df.columns:
            plt.figure(figsize=(10,6))
            sns.boxplot(x='Accident_Severity', y='Biker_Age', data=filtered_df, palette='viridis')
            show_plot('Biker Age by Accident Severity', 'Accident Severity', 'Biker Age')

        if "Bike_Speed" in filtered_df.columns:
            plt.figure(figsize=(10,6))
            sns.boxplot(x='Accident_Severity', y='Bike_Speed', data=filtered_df, palette='viridis')
            show_plot('Bike Speed by Accident Severity', 'Accident Severity', 'Bike Speed')

    # --- SCATTER PLOTS ---
    with st.expander("📉 Scatter Plots"):
        if all(x in filtered_df.columns for x in ["Bike_Speed", "Daily_Travel_Distance", "Accident_Severity"]):
            plt.figure(figsize=(10,6))
            sns.scatterplot(
                x='Bike_Speed', y='Daily_Travel_Distance', hue='Accident_Severity',
                data=filtered_df, palette='viridis', alpha=0.6
            )
            plt.legend(title='Accident Severity')
            show_plot('Speed vs Travel Distance by Accident Severity', 'Bike Speed', 'Daily Travel Distance')

# ====== FOOTER ======
st.markdown("---")
st.caption("© 2025 Road Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
