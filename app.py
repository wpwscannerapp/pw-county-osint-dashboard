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
st.markdown("**Real-time Open Source Intelligence for Prince William County, Virginia**")

# ========================
# DATABASE CONNECTION
# ========================
@st.cache_resource
def get_connection():
    return psycopg2.connect(DATABASE_URL, connect_timeout=10)

def load_incidents(limit=1000):
    conn = get_connection()
    query = f"""
        SELECT 
            created_at, title, description, category, incident_type, 
            location, latitude, longitude, source, sentiment
        FROM {SCHEMA}.incidents
        ORDER BY created_at DESC
        LIMIT %s
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

# Load data
df = load_incidents()

if df.empty:
    st.warning("No incidents found yet. Data collectors are running in the background via GitHub Actions.")
    st.stop()

# ========================
# SIDEBAR FILTERS
# ========================
st.sidebar.header("🔎 Filters")

locations = ['All'] + sorted(df['location'].dropna().unique())
selected_location = st.sidebar.selectbox("📍 Location", locations)

categories = ['All'] + sorted(df['category'].dropna().unique())
selected_category = st.sidebar.selectbox("📌 Category", categories)

# Apply filters
filtered_df = df.copy()
if selected_location != 'All':
    filtered_df = filtered_df[filtered_df['location'] == selected_location]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# ========================
# MAIN DASHBOARD
# ========================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Incidents", len(filtered_df))
with col2:
    st.metric("Last Updated", filtered_df['created_at'].max().strftime("%b %d, %H:%M") if not filtered_df.empty else "N/A")
with col3:
    st.metric("Sources", filtered_df['source'].nunique())
with col4:
    st.metric("Critical", len(filtered_df[filtered_df.get('is_critical', False)]))

tab1, tab2, tab3 = st.tabs(["📋 Live Incidents", "🗺️ Heatmap", "📊 Analytics"])

with tab1:
    st.dataframe(
        filtered_df[['created_at', 'location', 'category', 'title', 'description', 'source']],
        use_container_width=True,
        hide_index=True
    )

with tab2:
    if not filtered_df.empty and 'latitude' in filtered_df.columns:
        st.map(
            filtered_df.dropna(subset=['latitude', 'longitude']),
            latitude='latitude',
            longitude='longitude',
            size=20
        )
    else:
        st.info("No geographic data available yet.")

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Incidents by Category")
        if not filtered_df.empty:
            fig = px.pie(filtered_df, names='category', title="Category Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.subheader("Incidents Over Time")
        if not filtered_df.empty:
            filtered_df['date'] = pd.to_datetime(filtered_df['created_at']).dt.date
            time_df = filtered_df.groupby('date').size().reset_index(name='count')
            fig2 = px.line(time_df, x='date', y='count', title="Incident Trend")
            st.plotly_chart(fig2, use_container_width=True)

st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Hosted on Neon + Streamlit Cloud")
