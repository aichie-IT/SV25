import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Motorbike Accident Insights Dashboard",
                   page_icon="🏍️",
                   layout="wide")

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

    # --- THEME SELECTION ---
    st.markdown("### 🌓 Theme Settings")
    theme_mode = st.radio("Select Theme", ["Light 🌞", "Dark 🌙"])

    if theme_mode == "Light 🌞":
        bg_color = "#FAFAFA"
        text_color = "#000000"
        plotly_colors = px.colors.qualitative.Pastel
    else:
        bg_color = "#121212"
        text_color = "#FFFFFF"
        plotly_colors = px.colors.qualitative.Dark24

    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            color: {text_color};
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            border: 2px solid {'#999' if theme_mode=='Light 🌞' else '#FFD580'};
        ">
            {theme_mode} Mode
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- SUMMARY BOX ---
    st.markdown("### 🧾 Data Summary")
    st.info(f"**Total Records:** {len(df):,}\n\n**Columns:** {len(df.columns)}")

    # --- FILTERS ---
    with st.expander("🎯 Filter Options", expanded=True):
        st.markdown("Select filters to refine your dashboard view:")

        severity = st.selectbox("Accident Severity", ["All"] + sorted(df["Accident_Severity"].dropna().unique()))
        weather = st.selectbox("Weather Condition", ["All"] + sorted(df["Weather"].dropna().unique()))
        time_of_day = st.selectbox("Time of Day", ["All"] + sorted(df["Time_of_Day"].dropna().unique()))
        road_type = st.selectbox("Road Type", ["All"] + sorted(df["Road_Type"].dropna().unique()))

        if "Biker_Age" in df.columns:
            min_age, max_age = st.slider(
                "Biker Age",
                int(df["Biker_Age"].min()),
                int(df["Biker_Age"].max()),
                (int(df["Biker_Age"].min()), int(df["Biker_Age"].max()))
            )
        else:
            min_age, max_age = None, None

        # Optional: Add alcohol filter
        if "Biker_Alcohol" in df.columns:
            alcohol = st.selectbox("Biker Alcohol Consumption", ["All"] + sorted(df["Biker_Alcohol"].dropna().unique()))
        else:
            alcohol = "All"

        # --- APPLY FILTERS ---
        filtered_df = df.copy()
        if severity != "All": filtered_df = filtered_df[filtered_df["Accident_Severity"]==severity]
        if weather != "All": filtered_df = filtered_df[filtered_df["Weather"]==weather]
        if time_of_day != "All": filtered_df = filtered_df[filtered_df["Time_of_Day"]==time_of_day]
        if road_type != "All": filtered_df = filtered_df[filtered_df["Road_Type"]==road_type]
        if min_age is not None: filtered_df = filtered_df[(filtered_df["Biker_Age"]>=min_age) & (filtered_df["Biker_Age"]<=max_age)]
        if alcohol != "All": filtered_df = filtered_df[filtered_df["Biker_Alcohol"]==alcohol]

    # --- RESET BUTTON ---
    if st.button("🔄 Reset Filters"):
        st.session_state.clear()
        st.experimental_rerun()

    st.caption("Designed with ❤️ using Streamlit")

# ====== MAIN TITLE ======
st.markdown(f"<h1 style='color:{text_color}'>🏍️ Motorbike Accident Insights Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{text_color}'>Explore accident patterns and biker behaviors with interactive visual analytics.</p>", unsafe_allow_html=True)
st.markdown("---")

# ====== METRICS ======
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", f"{len(filtered_df):,}")
col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f} years")
col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h")
col4.metric("Avg. Travel Distance", f"{filtered_df['Daily_Travel_Distance'].mean():.1f} km")
st.markdown("---")

# ====== TABS ======
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚙️ Overview","📊 Factors","📈 Numerical","📉 Advanced","🗺️ Map"])

# --- TAB 1: Overview ---
with tab1:
    st.subheader("Distribution Overview")
    col1, col2, col3 = st.columns(3)
    # Pie charts
    pie_data = {
        "Accident Severity": filtered_df["Accident_Severity"].value_counts(),
        "Helmet Usage": filtered_df["Wearing_Helmet"].value_counts(),
        "Valid License": filtered_df["Valid_Driving_License"].value_counts()
    }
    for col, (title, data) in zip([col1,col2,col3], pie_data.items()):
        fig = px.pie(data.reset_index(), values=data.values, names=data.index,
                     title=title, color_discrete_sequence=plotly_colors,
                     template="plotly_dark" if theme_mode=="Dark 🌙" else "plotly_white")
        col.plotly_chart(fig, use_container_width=True)

# --- TAB 2: Factors ---
with tab2:
    st.subheader("Accident Severity by Categorical Factors")
    categorical_cols = [
        "Biker_Occupation","Biker_Education_Level",
        "Wearing_Helmet","Motorcycle_Ownership","Valid_Driving_License",
        "Bike_Condition","Road_Type","Road_condition","Weather",
        "Time_of_Day","Traffic_Density","Biker_Alcohol"
    ]
    for i in range(0, len(categorical_cols), 2):
        c1, c2 = st.columns(2)
        for j, col_name in enumerate(categorical_cols[i:i+2]):
            if col_name in filtered_df.columns:
                agg = filtered_df.groupby([col_name,"Accident_Severity"]).size().reset_index(name="Count")
                fig = px.bar(agg, x=col_name, y="Count", color="Accident_Severity", barmode="group",
                             color_discrete_sequence=plotly_colors,
                             template="plotly_dark" if theme_mode=="Dark 🌙" else "plotly_white",
                             title=f"{col_name.replace('_',' ')} vs Accident Severity")
                if j==0: c1.plotly_chart(fig,use_container_width=True)
                else: c2.plotly_chart(fig,use_container_width=True)

# --- TAB 3: Numerical Analysis ---
with tab3:
    st.subheader("Distribution of Numeric Variables")
    numeric_cols = ["Biker_Age","Bike_Speed","Riding_Experience","Daily_Travel_Distance"]
    col1, col2 = st.columns(2)
    for col_plot, col_name in zip([col1,col2]*2, numeric_cols):
        if col_name in filtered_df.columns:
            fig = px.histogram(filtered_df, x=col_name, nbins=20, color_discrete_sequence=plotly_colors,
                               template="plotly_dark" if theme_mode=="Dark 🌙" else "plotly_white",
                               title=f"Distribution of {col_name.replace('_',' ')}")
            col_plot.plotly_chart(fig,use_container_width=True)

# --- TAB 4: Advanced Visualizations ---
with tab4:
    st.subheader("Advanced Statistical Visualizations")
    sns.set_style("whitegrid" if theme_mode=="Light 🌞" else "darkgrid")
    plt.rcParams.update({
        'axes.facecolor': bg_color,
        'figure.facecolor': bg_color,
        'text.color': text_color,
        'axes.labelcolor': text_color,
        'xtick.color': text_color,
        'ytick.color': text_color
    })

    def show_plot(title,xlabel,ylabel,rotation=False):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if rotation: plt.xticks(rotation=45,ha='right')
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.clf()

    # Example Box Plot
    if "Biker_Age" in filtered_df.columns:
        plt.figure(figsize=(12,7))
        sns.boxplot(x='Accident_Severity',y='Biker_Age',data=filtered_df,palette='viridis')
        show_plot("Biker Age by Accident Severity","Accident Severity","Biker Age")

# --- TAB 5: Map ---
with tab5:
    st.subheader("🗺️ Geographical Distribution")
    if "Latitude" in filtered_df.columns and "Longitude" in filtered_df.columns:
        st.map(filtered_df[["Latitude","Longitude"]])
    else:
        st.warning("Map data not available in this dataset.")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Motorbike Accident Dashboard | Designed with ❤️ using Streamlit & Plotly")
