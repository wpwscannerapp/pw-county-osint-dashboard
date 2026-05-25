import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import plotly.express as px

from config import DATABASE_URL, SCHEMA

st.set_page_config(
    page_title="PWC OSINT Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Prince William County OSINT Dashboard")
st.markdown("Real-time incident monitoring for Prince William County, VA")

# ========================
# DATABASE CONNECTION
# ========================
@st.cache_resource
def get_connection():
    return psycopg2.connect(DATABASE_URL)

def load_incidents(limit=500):
    conn = get_connection()
    query = f"""
        SELECT 
            id, title, description, category, incident_type, location,
            latitude, longitude, source, source_url, sentiment, created_at
        FROM {SCHEMA}.incidents
        ORDER BY created_at DESC
        LIMIT %s
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

# ========================
# SIDEBAR FILTERS
# ========================
st.sidebar.header("Filters")

df = load_incidents()

if df.empty:
    st.warning("No incidents found yet. Collectors are running in background.")
else:
    # Location filter
    locations = ['All'] + sorted(df['location'].unique())
    selected_location = st.sidebar.selectbox("Location", locations)

    # Category filter
    categories = ['All'] + sorted(df['category'].unique())
    selected_category = st.sidebar.selectbox("Category", categories)

    # Apply filters
    filtered_df = df.copy()
    if selected_location != 'All':
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    # ========================
    # MAIN DASHBOARD
    # ========================
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Incidents", len(filtered_df))
    with col2:
        st.metric("Last Updated", filtered_df['created_at'].max().strftime("%H:%M") if not filtered_df.empty else "N/A")
    with col3:
        st.metric("Sources", filtered_df['source'].nunique())

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Live Incidents", "Heatmap", "Analytics"])

    with tab1:
        st.dataframe(
            filtered_df[['created_at', 'location', 'category', 'title', 'description', 'source']],
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        if not filtered_df.empty and 'latitude' in filtered_df.columns:
            st.map(
                filtered_df,
                latitude='latitude',
                longitude='longitude',
                size=20,
                color='category'
            )
        else:
            st.info("No location data available yet.")

    with tab3:
        if not filtered_df.empty:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Incidents by Category")
                fig = px.pie(filtered_df, names='category', title="Category Breakdown")
                st.plotly_chart(fig, use_container_width=True)
            
            with col_b:
                st.subheader("Incidents Over Time")
                filtered_df['date'] = pd.to_datetime(filtered_df['created_at']).dt.date
                time_df = filtered_df.groupby('date').size().reset_index(name='count')
                fig2 = px.line(time_df, x='date', y='count', title="Incidents Trend")
                st.plotly_chart(fig2, use_container_width=True)

# Footer
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data from pwc_osint schema")
