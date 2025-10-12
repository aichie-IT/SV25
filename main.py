import streamlit as st

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Scientific Visualization", divider="gray")


# --- Assume arts_df is defined and loaded here ---
# (For the app to run as a standalone example, we'll create a dummy DataFrame)
data = {'Gender': ['Female', 'Male', 'Female', 'Female', 'Male', 'Other', 'Female', 'Male', 'Male', 'Female']}
arts_df = pd.DataFrame(data)
# --------------------------------------------------

# 1. Calculate the gender counts
gender_counts = arts_df['Gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count'] # Rename columns for Plotly

st.header("Distribution of Gender in Arts Faculty", divider="gray")

# --- Plotly Pie Chart (replacing Matplotlib Pie Chart) ---

# Create the Plotly figure
fig_pie = px.pie(
    gender_counts, 
    values='Count', 
    names='Gender', 
    title='Distribution of Gender in Arts Faculty',
    hole=.3 # Optional: makes it a donut chart
)

# Display the Plotly figure in Streamlit
st.subheader("Pie Chart")
st.plotly_chart(fig_pie, use_container_width=True)


# --- Plotly Bar Chart (replacing Matplotlib Bar Chart) ---

# Create the Plotly figure
fig_bar = px.bar(
    gender_counts, 
    x='Gender', 
    y='Count', 
    title='Distribution of Gender in Arts Faculty',
    color='Gender' # Assign color by gender
)

# Customize the bar chart layout (optional)
fig_bar.update_layout(
    xaxis_title='Gender',
    yaxis_title='Count',
    xaxis={'categoryorder':'total descending'} # Order bars by count
)

# Display the Plotly figure in Streamlit
st.subheader("Bar Chart")
st.plotly_chart(fig_bar, use_container_width=True)
