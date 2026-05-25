import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

st.set_page_config(
    page_title="PWC OSINT Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Prince William County OSINT Dashboard")
st.markdown("**Real-time** incident monitoring for Police, Fire, Rescue & Local News in Prince William County, VA")

# ======================== SUPABASE CONNECTION ========================
@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# ======================== LOAD DATA ========================
@st.cache_data(ttl=60)
def load_incidents(limit=500):
    try:
        response = supabase.table("pwc_osint.incidents") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        st.info("Make sure your collectors have run at least once.")
        return pd.DataFrame()

df = load_incidents()

if df.empty:
    st.warning("⚠️ No incidents found yet.")
    st.info("→ Go to **GitHub → Actions** and manually run the 'OSINT Data Collectors' workflow.")
    st.stop()

# ======================== FILTERS ========================
st.sidebar.header("🔍 Filters")

# Safe column handling
loc_col = 'location' if 'location' in df.columns else None
cat_col = 'category' if 'category' in df.columns else 'type' if 'type' in df.columns else None

locations = ['All'] + sorted(df[loc_col].dropna().unique().tolist()) if loc_col else ['All']
selected_location = st.sidebar.selectbox("📍 Location", locations)

categories = ['All'] + sorted(df[cat_col].dropna().unique().tolist()) if cat_col else ['All']
selected_category = st.sidebar.selectbox("📌 Category", categories)

# Apply filters
filtered_df = df.copy()
if selected_location != 'All' and loc_col:
    filtered_df = filtered_df[filtered_df[loc_col] == selected_location]
if selected_category != 'All' and cat_col:
    filtered_df = filtered_df[filtered_df[cat_col] == selected_category]

# ======================== METRICS ========================
col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", len(filtered_df))
col2.metric("Last Updated", 
            filtered_df['created_at'].max()[:16] if not filtered_df.empty else "
