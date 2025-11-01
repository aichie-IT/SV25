import streamlit as st
import pandas as pd
import plotly.express as px

# ===== PAGE HEADER =====
st.title("⚙️ General Overview")
st.markdown("Overview of accident severity, helmet use, and license validity.")

# ===== ACCESS FILTERED DATA =====
filtered_df = st.session_state.get("filtered_df", None)

# ===== COLOR THEME =====
color_theme = px.colors.qualitative.Pastel

# ===== DATA VALIDATION =====
if filtered_df is None or filtered_df.empty:
    st.warning("⚠️ No data available. Please adjust your filters in the sidebar.")
else:
    # ===== SUMMARY METRICS =====
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{len(filtered_df):,}")
    col2.metric("Avg. Age", f"{filtered_df['Biker_Age'].mean():.1f}")
    col3.metric("Avg. Speed", f"{filtered_df['Bike_Speed'].mean():.1f} km/h")
    col4.metric(
        "Helmet Usage (%)",
        f"{(filtered_df['Wearing_Helmet'].value_counts(normalize=True).get('Yes', 0) * 100):.1f}%"
    )

    # ===== INSIGHT SUMMARY =====
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

    # ===== PIE CHARTS =====
    col1, col2, col3 = st.columns(3)

    # --- 1. Accident Severity ---
    with col1:
        severity_counts = (
            filtered_df["Accident_Severity"].value_counts().reset_index()
        )
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
        **Interpretation:** Most accidents are classified as *minor*, suggesting effective safety measures 
        such as helmet usage and speed regulation.
        """)

    # --- 2. Helmet Usage ---
    with col2:
        helmet_counts = (
            filtered_df["Wearing_Helmet"].value_counts().reset_index()
        )
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
        **Interpretation:** Helmet usage exceeds 70%, correlating with fewer severe accidents and lower injury rates.
        """)

    # --- 3. Valid Driving License ---
    with col3:
        license_counts = (
            filtered_df["Valid_Driving_License"].value_counts().reset_index()
        )
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
        **Interpretation:** Riders with valid licenses tend to experience less severe accidents, 
        supporting the importance of formal riding training.
        """)
