import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


# --- PAGE CONFIG ---
st.set_page_config(page_title="Motorbike Accident Insights Dashboard", page_icon="🏍️", layout="wide")

# --- COLOR THEME ---
color_theme = px.colors.qualitative.Pastel

# --- LOAD DATA ---
url = "https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/motor_accident.csv"
df = pd.read_csv(url)

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")

# Select Accident Severity
severity_options = df["Accident_Severity"].dropna().unique().tolist()
selected_severity = st.sidebar.multiselect(
    "Select Accident Severity:",
    options=severity_options,
    default=severity_options
)

# Filtered dataset
filtered_df = df[df["Accident_Severity"].isin(selected_severity)]

# --- MAIN TITLE ---
st.title("🏍️ Motorbike Accident Insights Dashboard")
st.markdown("Explore accident patterns and biker behaviors with interactive visual analytics.")

st.markdown("---")

# --- SUMMARY CARDS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", f"{len(filtered_df):,}", help="PLO 1: Total Motor Accident Records", border=True)
col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f} years", help="PLO 2: Average Biker Age", border=True)
col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h", help="PLO 3: Average Bike Speed", border=True)
col4.metric("Avg. Travel Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km", help="PLO 4: Avarege Daily Travel Distance", border=True)

st.markdown("---")

# --- TAB LAYOUT ---
tab1, tab2, tab3, tab4 = st.tabs(["⚙️ General Overview", "📊 Accident Factors", "📈 Numerical Analysis", "📉 Advanced Visualizations"])

# ============ TAB 1: GENERAL OVERVIEW ============
with tab1:
    st.subheader("Distribution Overview")

    col1, col2, col3 = st.columns(3)

    # Pie: Accident Severity
    with col1:
        severity_counts = filtered_df["Accident_Severity"].value_counts().reset_index()
        severity_counts.columns = ["Accident_Severity", "Count"]
        fig1 = px.pie(
            severity_counts, 
            values="Count", 
            names="Accident_Severity",
            title="Accident Severity Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Pie: Helmet Usage
    with col2:
        helmet_counts = filtered_df["Wearing_Helmet"].value_counts().reset_index()
        helmet_counts.columns = ["Wearing_Helmet", "Count"]
        fig2 = px.pie(
            helmet_counts, 
            values="Count", 
            names="Wearing_Helmet", 
            title="Wearing Helmet Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Pie: Valid License
    with col3:
        license_counts = filtered_df["Valid_Driving_License"].value_counts().reset_index()
        license_counts.columns = ["Valid_Driving_License", "Count"]
        fig3 = px.pie(
            license_counts, 
            values="Count", 
            names="Valid_Driving_License",
            title="Valid Driving License Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig3, use_container_width=True)

# ============ TAB 2: ACCIDENT FACTORS ============
with tab2:
    st.subheader("Accident Severity by Categorical Factors")

    # Occupation
    fig4 = px.bar(
        filtered_df,
        y="Biker_Occupation",
        color="Accident_Severity",
        title="Accident Severity by Biker Occupation",
        color_discrete_sequence=color_theme
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Education
    fig5 = px.bar(
        filtered_df,
        y="Biker_Education_Level",
        color="Accident_Severity",
        title="Accident Severity by Biker Education Level",
        color_discrete_sequence=color_theme
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Other Influencing Factors")

    categorical_cols = [
        "Wearing_Helmet", "Motorcycle_Ownership", "Valid_Driving_License",
        "Bike_Condition", "Road_Type", "Road_condition", "Weather",
        "Time_of_Day", "Traffic_Density", "Biker_Alcohol"
    ]

    for col in categorical_cols:
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
    st.subheader("Distribution of Numeric Variables")

    col1, col2 = st.columns(2)
    with col1:
        fig6 = px.histogram(
            filtered_df, x="Biker_Age", nbins=20,
            title="Distribution of Biker Age",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig6, use_container_width=True)

        fig7 = px.histogram(
            filtered_df, x="Bike_Speed", nbins=20,
            title="Distribution of Bike Speed",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        fig8 = px.histogram(
            filtered_df, x="Riding_Experience", nbins=20,
            title="Distribution of Riding Experience",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig8, use_container_width=True)

        fig9 = px.histogram(
            filtered_df, x="Daily_Travel_Distance", nbins=20,
            title="Distribution of Daily Travel Distance",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig9, use_container_width=True)

# ============ TAB 4: ADVANCED VISUALIZATIONS ============
with tab4:
    st.subheader("Advanced Statistical Visualizations")
    st.markdown("Explore deeper relationships using box, violin, and scatter plots.")
    
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
        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Biker_Age', data=filtered_df, palette='viridis')
        show_plot('Distribution of Biker Age by Accident Severity', 'Accident Severity', 'Biker Age')

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Riding_Experience', data=filtered_df, palette='viridis')
        show_plot('Distribution of Riding Experience by Accident Severity', 'Accident Severity', 'Riding Experience (Years)')

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Daily_Travel_Distance', data=filtered_df, palette='viridis')
        show_plot('Distribution of Daily Travel Distance by Accident Severity', 'Accident Severity', 'Daily Travel Distance')

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Bike_Speed', data=filtered_df, palette='viridis')
        show_plot('Distribution of Bike Speed by Accident Severity', 'Accident Severity', 'Bike Speed')

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Accident_Severity', y='Speed_Limit', data=filtered_df, palette='viridis')
        show_plot('Distribution of Speed Limit by Accident Severity', 'Accident Severity', 'Speed Limit')

        plt.figure(figsize=(12, 7))
        sns.boxplot(x='Biker_Occupation', y='Bike_Speed', data=filtered_df, palette='viridis')
        show_plot('Distribution of Bike Speed by Biker Occupation', 'Biker Occupation', 'Bike Speed', rotation=True)

    # --- VIOLIN PLOTS ---
    with st.expander("🎻 Violin Plots"):
        plt.figure(figsize=(12, 7))
        sns.violinplot(x='Accident_Severity', y='Biker_Age', data=filtered_df, palette='viridis')
        show_plot('Distribution of Biker Age by Accident Severity (Violin Plot)', 'Accident Severity', 'Biker Age')

        plt.figure(figsize=(12, 7))
        sns.violinplot(x='Weather', y='Bike_Speed', data=filtered_df, palette='viridis')
        show_plot('Distribution of Bike Speed by Weather (Violin Plot)', 'Weather', 'Bike Speed')

    # --- SCATTER PLOTS ---
    with st.expander("📈 Scatter Plots"):
        plt.figure(figsize=(14, 10))
        sns.scatterplot(x='Bike_Speed', y='Daily_Travel_Distance', hue='Accident_Severity', data=filtered_df, palette='viridis', alpha=0.6)
        plt.legend(title='Accident Severity')
        show_plot('Daily Travel Distance vs Bike Speed by Accident Severity', 'Bike Speed', 'Daily Travel Distance')

        plt.figure(figsize=(12, 8))
        sns.scatterplot(x='Bike_Speed', y='Biker_Age', data=filtered_df, alpha=0.6)
        show_plot('Biker Age vs Bike Speed', 'Bike Speed', 'Biker Age')

        plt.figure(figsize=(12, 8))
        sns.scatterplot(x='Daily_Travel_Distance', y='Biker_Age', data=filtered_df, alpha=0.6)
        show_plot('Biker Age vs Daily Travel Distance', 'Daily Travel Distance', 'Biker Age')


# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Motorbike Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
