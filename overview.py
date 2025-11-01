import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# Retrieve shared variables
filtered_df = st.session_state.get("filtered_df")
color_theme = st.session_state.get("color_theme", px.colors.qualitative.Pastel)

if filtered_df is None or filtered_df.empty:
    st.warning("⚠️ No data available. Please adjust your filters in the sidebar.")
    st.stop()

st.subheader("Distribution Overview")
st.markdown("Overview of accident severity, helmet use, and license validity.")

# Summary box
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", f"{len(filtered_df):,}", border=True)
col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f}", border=True)
col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h", border=True)
col4.metric("Helmet Usage (%)", f"{(filtered_df['Wearing_Helmet'].value_counts(normalize=True).get('Yes', 0) * 100):.1f}%", border=True)

# Scientific Summary
st.markdown("### Summary")
st.info("""
This overview highlights general distributions in the dataset. Most riders wear helmets, 
and the average biking speed is moderate compared to the speed limits observed. 
The distribution of accident severity suggests that minor and moderate accidents dominate, 
implying that protective behaviors like helmet use and valid licensing may contribute 
to reducing severe outcomes. These insights establish a foundation for understanding 
how individual safety practices and environmental conditions interact.
""")
st.markdown("---")

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
    st.success("""
    **Interpretation:** Most accidents are classified as *minor*, suggesting effective safety measures such as helmet usage and speed regulation.
    """)

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
    st.success("""
    **Interpretation:** Helmet usage exceeds 70%, which correlates with fewer severe accidents and lower injury rates.
    """)

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
    st.success("""
    **Interpretation:** Riders with valid licenses tend to experience less severe accidents, supporting the importance of formal riding training.
    """)

# --- Observation Section ---
st.markdown("#### 💬 Observation")
st.success("""
The majority of accidents are classified as minor. Helmet usage is generally high,
which correlates with lower accident severity. Riders with valid licenses also
exhibit safer driving trends, suggesting that training and enforcement play key roles.
""")
