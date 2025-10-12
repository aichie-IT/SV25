# 1. Define the URL for the data source
DATA_URL = 'https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/arts_faculty_data.csv'

# Streamlit page configuration
st.set_page_config(
    page_title="Scientific Visualization",
    layout="wide"
)

st.header("Distribution of Gender in Arts Faculty", divider="gray")

# --- 2. Data Loading and Caching ---

# Use Streamlit's caching to load data only once
@st.cache_data
def load_data(url):
    """Loads the CSV data from the URL."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

arts_df = load_data(DATA_URL)

# --- 3. Data Processing and Visualization ---

if not arts_df.empty and 'Gender' in arts_df.columns:
    
    # Calculate gender counts and reset index for Plotly structure
    gender_counts = arts_df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    # Display a preview of the data (replaces arts_df.head())
    st.subheader("Data Preview")
    st.dataframe(arts_df.head(), use_container_width=True)
    st.markdown("---")


    # --- 4. Plotly Pie Chart (Replacing Matplotlib Pie) ---
    st.subheader("Gender Distribution: Pie Chart")
    
    # Create the Plotly Pie figure
    fig_pie = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        title='Distribution of Gender in Arts Faculty (Percentage)',
        hole=0.4 # Optional: makes it a donut chart
    )
    
    # Customize text format
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("---")


    # --- 5. Plotly Bar Chart (Replacing Matplotlib Bar) ---
    st.subheader("Gender Distribution: Bar Chart")
    
    # Create the Plotly Bar figure
    fig_bar = px.bar(
        gender_counts,
        x='Gender',
        y='Count',
        title='Distribution of Gender in Arts Faculty (Count)',
        color='Gender' # Color the bars by Gender
    )
    
    # Customize bar chart layout for better readability
    fig_bar.update_layout(
        xaxis_title='Gender',
        yaxis_title='Count',
        # Sort bars by count in descending order
        xaxis={'categoryorder':'total descending'} 
    )

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("Cannot proceed. The data failed to load or the 'Gender' column is missing.")
