import streamlit as st
import plotly.express as px

color_theme = px.colors.qualitative.Pastel

def show_overview(filtered_df):
    st.subheader("Distribution Overview")
    st.markdown("Overview of accident severity, helmet use, and license validity.")

    if filtered_df.empty:
        st.warning("No data available for visualization.")
        return

    # --- Summary metrics ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{len(filtered_df):,}")
    col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f}")
    col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h")
    col4.metric("Helmet Usage (%)", f"{(filtered_df['Wearing_Helmet'].value_counts(normalize=True).get('Yes',0)*100):.1f}%")

    st.markdown("### Summary")
    st.info("""
    This overview highlights general distributions in the dataset. 
    Most riders wear helmets, and the average biking speed is moderate. 
    Minor accidents dominate, suggesting helmet use and valid licensing help reduce severe outcomes.
    """)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    # --- Pie: Severity ---
    with col1:
        severity_counts = filtered_df["Accident_Severity"].value_counts().reset_index()
        severity_counts.columns = ["Accident_Severity", "Count"]
        fig1 = px.pie(severity_counts, values="Count", names="Accident_Severity",
                      title="Accident Severity", color_discrete_sequence=color_theme)
        st.plotly_chart(fig1, use_container_width=True)

    # --- Pie: Helmet Usage ---
    with col2:
        helmet_counts = filtered_df["Wearing_Helmet"].value_counts().reset_index()
        helmet_counts.columns = ["Wearing_Helmet", "Count"]
        fig2 = px.pie(helmet_counts, values="Count", names="Wearing_Helmet",
                      title="Helmet Usage", color_discrete_sequence=color_theme)
        st.plotly_chart(fig2, use_container_width=True)

    # --- Pie: License Validity ---
    with col3:
        license_counts = filtered_df["Valid_Driving_License"].value_counts().reset_index()
        license_counts.columns = ["Valid_Driving_License", "Count"]
        fig3 = px.pie(license_counts, values="Count", names="Valid_Driving_License",
                      title="License Validity", color_discrete_sequence=color_theme)
        st.plotly_chart(fig3, use_container_width=True)

    # --- Observation ---
    st.markdown("#### 💬 Observation")
    st.success("""
    Minor accidents dominate the dataset, reflecting safer road behavior.
    Helmet compliance is high and positively linked to lower accident severity.
    Riders with valid licenses demonstrate safer patterns overall.
    """)
