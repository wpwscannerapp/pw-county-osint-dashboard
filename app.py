import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from config import SUPABASE_URL, SUPABASE_KEY, SCHEMA
from supabase import create_client, Client

st.set_page_config(
    page_title="PWC OSINT Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Prince William County OSINT Dashboard")
st.markdown("Real-time Open Source Intelligence for Police, Fire, Rescue & Local News")

# Initialize Supabase client
@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

@st.cache_data(ttl=60)  # Refresh every 60 seconds
def load_incidents(limit=500):
    try:
        response = supabase.table(f"{SCHEMA}.incidents") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return pd.DataFrame()

# Load data
df = load_incidents()

if df.empty:
    st.warning("⚠️ No incidents found yet. Your collectors are running via GitHub Actions.")
    st.info("First data should appear within 15-30 minutes after collectors run.")
    st.stop()

# ======================== SIDEBAR FILTERS ========================
st.sidebar.header("🔍 Filters")

# Location filter
locations = ['All'] + sorted(df['location'].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("📍 Location", locations)

# Category filter
categories = ['All'] + sorted(df['category'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("📌 Category", categories)

# Apply filters
filtered_df = df.copy()
if selected_location != 'All':
    filtered_df = filtered_df[filtered_df['location'] == selected_location]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# ======================== MAIN DASHBOARD ========================
col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", len(filtered_df))
col2.metric("Last Updated", 
            filtered_df['created_at'].max()[:16] if not filtered_df.empty else "N/A")
col3.metric("Sources", filtered_df['source'].nunique() if 'source' in filtered_df.columns else 0)

tab1, tab2, tab3 = st.tabs(["📋 Live Incidents", "🗺️ Heatmap", "📊 Analytics"])

with tab1:
    st.dataframe(
        filtered_df[['created_at', 'location', 'category', 'title', 'description', 'source']],
        use_container_width=True,
        hide_index=True
    )

with tab2:
    if not filtered_df.empty and 'latitude' in filtered_df.columns and filtered_df['latitude'].notna().any():
        st.map(
            filtered_df,
            latitude='latitude',
            longitude='longitude',
            size=20,
            color='category'
        )
    else:
        st.info("No location data available for mapping yet.")

with tab3:
    if not filtered_df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Incidents by Category")
            fig = px.pie(filtered_df, names='category', title="Category Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            st.subheader("
