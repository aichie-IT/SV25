import streamlit as st

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Scientific Visualization", divider="gray")


# 1. Define the URL for the data source
DATA_URL = "https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/arts_faculty_data.csv"

# Streamlit page configuration (from your initial prompt)
st.set_page_config(
    page_title="Scientific Visualization",
    layout="wide" # Use wide layout for better visualization space
)

st.header("Genetic Algorithm: Distribution of Gender in Arts Faculty", divider="gray")

# --- Data Loading and Processing ---

# Use Streamlit's caching decorator to load data only once
@st.cache_data
def load_data():
    """Loads the CSV data from the URL using pandas."""
    try:
        df = pd.read_csv(DATA_URL)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame({'Gender': ['Error']})

arts_df = load_data()

# Check if the required column exists before proceeding
if 'Gender' in arts_df.columns:
    # 2. Calculate the gender counts and format for Plotly
    gender_counts = arts_df['Gender'].value_counts().reset_index()
    # Rename columns for clarity in Plotly
    gender_counts.columns = ['Gender', 'Count']

    # --- Plotly Pie Chart (replacing Matplotlib) ---

    # 3. Create the Plotly figure (Pie Chart)
    fig = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        title='**Distribution of Gender in Arts Faculty**',
        color_discrete_sequence=px.colors.sequential.RdBu, # Optional: Customize colors
        hole=0.4 # Optional: makes it a donut chart
    )

    # Optional: Customize the appearance
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # 4. Display the Plotly figure using Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("The loaded CSV data does not contain a 'Gender' column. Please check the file structure.")

# Optional: Display the raw data
with st.expander("View Raw Data"):
    st.dataframe(arts_df)
