import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Define the URL for the data source
URL = 'https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/arts_faculty_data.csv'

# Set Streamlit page configuration
st.set_page_config(
    page_title="Scientific Visualization",
    layout="wide" 
)

st.title("Arts Faculty Data Analysis")
st.markdown("---")

# --- 1. Data Loading and Caching ---

@st.cache_data
def load_data(url):
    """Loads the CSV data from the URL, using caching for efficiency."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data from URL: {url}\n{e}")
        return pd.DataFrame() # Return empty DataFrame on failure

arts_df = load_data(URL)

if arts_df.empty:
    st.stop() # Stop execution if data loading failed

# --- 2. Data Cleaning and Preparation for Visualizations ---

# Coerce GPA columns to numeric for calculation (as done in the original code)
arts_df['S.S.C (GPA)'] = pd.to_numeric(arts_df['S.S.C (GPA)'], errors='coerce')
arts_df['H.S.C (GPA)'] = pd.to_numeric(arts_df['H.S.C (GPA)'], errors='coerce')

# Define numerical survey columns for the correlation heatmap
NUMERICAL_Q_COLUMNS = [
    'Q3 [What was your expectation about the University as related to quality of resources?]',
    'Q4 [What was your expectation about the University as related to quality of learning environment?]',
    'Q5 [To what extent your expectation was met?]',
    # Include other numerical columns if necessary, the original list was short
]


# --- 3. Visualization Sections ---

st.header("1. Gender and Program Analysis")
col1, col2 = st.columns(2)

# --- A. Gender Distribution (Pie Chart & Bar Chart) ---
if 'Gender' in arts_df.columns:
    gender_counts_df = arts_df['Gender'].value_counts().reset_index()
    gender_counts_df.columns = ['Gender', 'Count']

    with col1:
        st.subheader("Gender Distribution (Pie Chart)")
        fig_pie = px.pie(
            gender_counts_df,
            values='Count',
            names='Gender',
            title='Gender Percentage',
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Gender vs. Arts Program (Stacked Bar)")
        # Calculate counts for stacked bar plot
        gender_program_counts = arts_df.groupby(['Gender', 'Arts Program']).size().reset_index(name='Count')
        
        fig_stacked_bar = px.bar(
            gender_program_counts, 
            x='Gender', 
            y='Count', 
            color='Arts Program',
            title='Count by Gender and Program'
        )
        st.plotly_chart(fig_stacked_bar, use_container_width=True)
else:
    st.warning("Skipping Gender analysis: 'Gender' column not found.")

st.markdown("---")
st.header("2. Academic Performance Distribution (Histograms)")
col3, col4, col5 = st.columns(3)

# --- B. H.S.C (GPA) Histogram ---
with col3:
    st.subheader("H.S.C (GPA) Distribution")
    if 'H.S.C (GPA)' in arts_df.columns:
        fig_hsc_hist = px.histogram(
            arts_df.dropna(subset=['H.S.C (GPA)']), 
            x='H.S.C (GPA)', 
            nbins=10, 
            title='H.S.C (GPA) Level'
        )
        st.plotly_chart(fig_hsc_hist, use_container_width=True)
    else:
        st.info("H.S.C (GPA) column not found.")

# --- C. S.S.C (GPA) Histogram ---
with col4:
    st.subheader("S.S.C (GPA) Distribution")
    if 'S.S.C (GPA)' in arts_df.columns:
        fig_ssc_hist = px.histogram(
            arts_df.dropna(subset=['S.S.C (GPA)']), 
            x='S.S.C (GPA)', 
            nbins=10, 
            title='S.S.C (GPA) Level'
        )
        st.plotly_chart(fig_ssc_hist, use_container_width=True)
    else:
        st.info("S.S.C (GPA) column not found.")

# --- D. Coaching Center Score Distribution (Histogram) ---
with col5:
    st.subheader("Coaching Center Attendance")
    coaching_col = 'Did you ever attend a Coaching center?'
    if coaching_col in arts_df.columns:
        fig_coaching_hist = px.histogram(
            arts_df, 
            x=coaching_col, 
            title='Coaching Center Score Distribution'
        )
        st.plotly_chart(fig_coaching_hist, use_container_width=True)
    else:
        st.info(f"'{coaching_col}' column not found.")


st.markdown("---")
st.header("3. Correlation and Relationship Analysis")

# --- E. S.S.C vs H.S.C Scatter Plot ---
st.subheader("S.S.C (GPA) vs. H.S.C (GPA) Scatter Plot")
scatter_data = arts_df.dropna(subset=['S.S.C (GPA)', 'H.S.C (GPA)'])

if not scatter_data.empty:
    fig_scatter = px.scatter(
        scatter_data, 
        x='S.S.C (GPA)', 
        y='H.S.C (GPA)', 
        title='Relationship between S.S.C and H.S.C GPAs',
        hover_data=['Gender', 'Arts Program'] # Add hover details for interactivity
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Skipping Scatter Plot: Not enough valid data points in S.S.C (GPA) and H.S.C (GPA).")
