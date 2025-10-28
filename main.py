import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

# --- Page Setup ---
st.set_page_config(
    page_title="Motorbike Insights Dashboard",
    page_icon="🏍️",
    layout="wide"
)

# --- Theme Colors ---
color_theme = px.colors.sequential.Viridis

# --- Load Dataset ---
url = https://raw.githubusercontent.com/aichie-IT/SV25/refs/heads/main/motor_accident.csv"
df = pd.read_csv(url)

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Data")

brand_options = sorted(df["Brand"].dropna().unique())
type_options = sorted(df["Type"].dropna().unique())

selected_brand = st.sidebar.multiselect(
    "Select Brand:",
    options=brand_options,
    default=brand_options
)

selected_type = st.sidebar.multiselect(
    "Select Type:",
    options=type_options,
    default=type_options
)

# --- Filter Data ---
filtered_df = df[
    (df["Brand"].isin(selected_brand)) &
    (df["Type"].isin(selected_type))
]

# --- Main Header ---
st.title("🏍️ Motorbike Insights Dashboard")
st.markdown("Explore performance, pricing, and specifications of various motorbike brands and models.")

st.markdown("---")

# --- Summary Boxes ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Motorbikes", f"{len(filtered_df):,}", help="Total number of motorbikes in dataset")

with col2:
    avg_price = filtered_df["Price"].mean()
    st.metric("Average Price", f"${avg_price:,.0f}", help="Average selling price")

with col3:
    avg_mileage = filtered_df["Mileage"].mean()
    st.metric("Average Mileage", f"{avg_mileage:.1f} km/l", help="Average mileage (fuel efficiency)")

with col4:
    unique_brands = filtered_df["Brand"].nunique()
    st.metric("Number of Brands", f"{unique_brands}", help="Unique motorbike brands available")

st.markdown("---")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Overview", "⚙️ Performance", "💬 Features"])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.subheader("📈 Motorbike Distribution Overview")

    col1, col2 = st.columns(2)

    with col1:
        brand_counts = filtered_df["Brand"].value_counts().reset_index()
        brand_counts.columns = ["Brand", "Count"]
        fig_brand = px.pie(
            brand_counts,
            values="Count",
            names="Brand",
            title="Market Share by Brand",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig_brand, use_container_width=True)

    with col2:
        type_counts = filtered_df["Type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        fig_type = px.bar(
            type_counts,
            x="Type",
            y="Count",
            title="Motorbike Count by Type",
            color="Count",
            color_continuous_scale=color_theme
        )
        fig_type.update_layout(xaxis_title="Type", yaxis_title="Count")
        st.plotly_chart(fig_type, use_container_width=True)

    st.subheader("Average Price by Brand")
    fig_price_brand = px.bar(
        filtered_df.groupby("Brand")["Price"].mean().reset_index(),
        x="Brand",
        y="Price",
        title="Average Price per Brand",
        color="Price",
        color_continuous_scale=color_theme
    )
    fig_price_brand.update_layout(xaxis_title="Brand", yaxis_title="Average Price")
    st.plotly_chart(fig_price_brand, use_container_width=True)

# --- TAB 2: PERFORMANCE ---
with tab2:
    st.subheader("⚙️ Performance Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig_mileage = px.histogram(
            filtered_df,
            x="Mileage",
            nbins=15,
            title="Distribution of Mileage (km/l)",
            color_discrete_sequence=color_theme
        )
        fig_mileage.update_layout(xaxis_title="Mileage (km/l)", yaxis_title="Count")
        st.plotly_chart(fig_mileage, use_container_width=True)

    with col2:
        fig_engine = px.histogram(
            filtered_df,
            x="Engine_Capacity",
            nbins=15,
            title="Distribution of Engine Capacity (cc)",
            color_discrete_sequence=color_theme
        )
        fig_engine.update_layout(xaxis_title="Engine Capacity (cc)", yaxis_title="Count")
        st.plotly_chart(fig_engine, use_container_width=True)

    st.subheader("Price vs Engine Capacity")
    fig_scatter = px.scatter(
        filtered_df,
        x="Engine_Capacity",
        y="Price",
        color="Brand",
        size="Mileage",
        hover_data=["Model"],
        title="Price vs Engine Capacity by Brand",
        color_discrete_sequence=color_theme
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- TAB 3: FEATURES ---
with tab3:
    st.subheader("💬 Feature Preferences & Insights")

    col1, col2 = st.columns(2)

    with col1:
        transmission_counts = filtered_df["Transmission"].value_counts().reset_index()
        transmission_counts.columns = ["Transmission", "Count"]
        fig_transmission = px.bar(
            transmission_counts,
            x="Transmission",
            y="Count",
            title="Transmission Type Distribution",
            color="Count",
            color_continuous_scale=color_theme
        )
        st.plotly_chart(fig_transmission, use_container_width=True)

    with col2:
        fuel_counts = filtered_df["Fuel_Type"].value_counts().reset_index()
        fuel_counts.columns = ["Fuel_Type", "Count"]
        fig_fuel = px.pie(
            fuel_counts,
            values="Count",
            names="Fuel_Type",
            title="Fuel Type Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig_fuel, use_container_width=True)

    st.subheader("Top 10 Models by Price")
    top_models = filtered_df.nlargest(10, "Price")
    fig_top_models = px.bar(
        top_models,
        x="Model",
        y="Price",
        color="Brand",
        title="Top 10 Most Expensive Motorbikes",
        color_discrete_sequence=color_theme
    )
    st.plotly_chart(fig_top_models, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("© 2025 Motorbike Dashboard | Designed with ❤️ using Streamlit & Plotly")
