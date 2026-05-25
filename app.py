import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Use the official Streamlit Supabase connection
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="PWC OSINT Dashboard", page_icon="🚨", layout="wide")

st.title("🚨 Prince William County OSINT Dashboard")
st.markdown("Real-time incident monitoring")

# Initialize Supabase connection
conn = st.connection("supabase", type=SupabaseConnection)

@st.cache_data(ttl=60)  # Refresh every minute
def load_incidents():
    try:
        response = conn.table("pwc_osint.incidents").select("*").order("created_at", desc=True).limit(500).execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

df = load_incidents()

if df.empty:
    st.warning("No incidents found yet. Collectors should be running via GitHub Actions.")
    st.stop()

# Filters
st.sidebar.header("Filters")
locations = ['All'] + sorted(df['location'].unique().tolist())
selected_location = st.sidebar.selectbox("Location", locations)

categories = ['All'] + sorted(df['category'].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

# Apply filters
filtered = df.copy()
if selected_location != 'All':
    filtered = filtered[filtered['location'] == selected_location]
if selected_category != 'All':
    filtered = filtered[filtered['category'] == selected_category]

# Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", len(filtered))
col2.metric("Last Updated", filtered['created_at'].max() if not filtered.empty else "N/A")
col3.metric("Sources", filtered['source'].nunique() if 'source' in filtered.columns else 0)

tab1, tab2, tab3 = st.tabs(["Live Incidents", "Heatmap", "Analytics"])

with tab1:
    st.dataframe(filtered, use_container_width=True, hide_index=True)

with tab2:
    if not filtered.empty and 'latitude' in filtered.columns:
        st.map(filtered, latitude='latitude', longitude='longitude')
    else:
        st.info("No location data available.")

with tab3:
    if not filtered.empty:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(filtered, names='category', title="Incidents by Category")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            filtered['date'] = pd.to_datetime(filtered['created_at']).dt.date
            trend = filtered.groupby('date').size().reset_index(name='count')
            fig2 = px.line(trend, x='date', y='count', title="Trend Over Time")
            st.plotly_chart(fig2, use_container_width=True)

st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
