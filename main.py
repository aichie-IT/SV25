import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Define the URL for the data source
URL = 'https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/arts_faculty_data.csv'

# Set Streamlit page configuration
st.set_page_config(
    page_title="Scientific Visualization",
    layout="wide" 
)

st.title("Distribution of Gender in Arts Faculty")
st.markdown("---")

# --- Data Loading and Caching ---

# Use Streamlit's caching decorator to load data only once
# This is crucial for performance in a web application
@st.cache_data
def load_data(url):
    """Loads the CSV data from the URL."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data from URL: {url}\n{e}")
        return pd.DataFrame() # Return empty DataFrame on failure

arts_df = load_data(URL)

if arts_df.empty:
    st.stop() # Stop execution if data loading failed

# --- 1. Data Preview (replacing display(arts_df.head())) ---
st.subheader("1. Data Preview")
st.dataframe(arts_df.head(), use_container_width=True)


# --- 2. Data Processing and Visualization ---

if 'Gender' in arts_df.columns:
    # Calculate the gender counts and format for Plotly
    gender_counts_df = arts_df['Gender'].value_counts().reset_index()
    # Rename columns for clarity in Plotly
    gender_counts_df.columns = ['Gender', 'Count']

    col1, col2 = st.columns(2)

    # --- Plotly Pie Chart (replacing Matplotlib Pie Chart) ---
    with col1:
        st.subheader("2. Gender Distribution (Pie Chart)")
        fig_pie = px.pie(
            gender_counts_df,
            values='Count',
            names='Gender',
            title='**Gender Distribution**',
            hole=0.4 # Makes it a donut chart
        )
        # Customize appearance
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        
        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Plotly Bar Chart (replacing Matplotlib Bar Chart) ---
    with col2:
        st.subheader("3. Gender Distribution (Bar Chart)")
        fig_bar = px.bar(
            gender_counts_df,
            x='Gender',
            y='Count',
            title='**Gender Count**',
            color='Gender'
        )

        # Customize the bar chart layout to sort by count (total descending)
        fig_bar.update_layout(
            xaxis_title='Gender',
            yaxis_title='Count',
            xaxis={'categoryorder':'total descending'}
        )

        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("The loaded CSV data does not contain a 'Gender' column required for visualization.")
