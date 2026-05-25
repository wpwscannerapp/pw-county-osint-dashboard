import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

st.set_page_config(page_title="PWC OSINT Dashboard", page_icon="🚨", layout="wide")

st.title("🚨 Prince William County OSINT Dashboard")
st.markdown("Real-time Open Source Intelligence for Prince William County, VA")

# Initialize Supabase
@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

@st.cache_data(ttl=60)
def load_incidents(limit=500):
    try:
        response = supabase.table("incidents") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        return pd.DataFrame()

df = load_incidents()

if df.empty:
    st.warning("⚠️ No incidents found yet.")
    st.info("Run the GitHub Actions collectors or check your table in Supabase.")
    st.stop()

# Debug: Show available columns
st.sidebar.write("**Available Columns:**", list(df.columns))

# Safe Filters
st.sidebar.header("🔍 Filters")

location_col = 'location' if 'location' in df.columns else None
category_col = 'category' if 'category' in df.columns else 'type'  # fallback

locations = ['All'] + sorted(df[location_col].dropna().unique().tolist()) if location_col else ['All']
selected_location = st.sidebar.selectbox("📍 Location", locations)

categories = ['All'] + sorted(df[category_col].dropna().unique().tolist()) if category_col in df.columns else ['All']
selected_category = st.sidebar.selectbox("📌 Category", categories)

# Apply filters safely
filtered_df = df.copy()
if selected_location != 'All' and location_col:
    filtered_df = filtered_df[filtered_df[location_col] == selected_location]
if selected_category != 'All' and category_col in df.columns:
    filtered_df = filtered_df[filtered_df[category_col] == selected_category]

# Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", len(filtered_df))
col2.metric("Last Updated", filtered_df['created_at'].max()[:16] if not filtered_df.empty else "—")
col3.metric("Sources", filtered_df.get('source', pd.Series()).nunique())

tab1, tab2, tab3 = st.tabs(["📋 Live Incidents", "🗺️ Heatmap", "📊 Analytics"])

with tab1:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with tab2:
    if not filtered_df.empty and 'latitude' in filtered_df.columns and filtered_df['latitude'].notna().any():
        st.map(filtered_df, latitude='latitude', longitude='longitude', size=20)
    else:
        st.info("No location data available yet.")

with tab3:
    if not filtered_df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("By Category")
            cat_col = category_col if category_col in filtered_df.columns else 'type'
            if cat_col in filtered_df.columns:
                fig = px.pie(filtered_df, names=cat_col)
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Over Time")
            if 'created_at' in filtered_df.columns:
                filtered_df['date'] = pd.to_datetime(filtered_df['created_at']).dt.date
                trend = filtered_df.groupby('date').size().reset_index(name='count')
                fig2 = px.line(trend, x='date', y='count')
                st.plotly_chart(fig2, use_container_width=True)

st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
