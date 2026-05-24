import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from config import (
    DATABASE_URL, DASHBOARD_CONFIG, PWC_LOCATIONS, DASHBOARD_COLORS,
    INCIDENT_KEYWORDS
)

# Page configuration
st.set_page_config(
    page_title=DASHBOARD_CONFIG['page_title'],
    page_icon=DASHBOARD_CONFIG['icon'],
    layout=DASHBOARD_CONFIG['layout'],
    initial_sidebar_state='expanded'
)

st.markdown("""
    <style>
    .reportview-container { margin-top: -2rem; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def get_recent_incidents(hours=24, limit=100):
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT 
                id, title, description, location, category, 
                incident_type, source, source_url, latitude, longitude,
                sentiment, created_at, updated_at
            FROM incidents
            WHERE created_at >= NOW() - INTERVAL '%s hours'
            ORDER BY created_at DESC
            LIMIT %s
        """
        cursor.execute(query, (hours, limit))
        incidents = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return pd.DataFrame(incidents) if incidents else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching incidents: {e}")
        return pd.DataFrame()

def get_incident_stats(hours=24):
    conn = get_db_connection()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT COUNT(*) as total FROM incidents
            WHERE created_at >= NOW() - INTERVAL '%s hours'
        """, (hours,))
        total = cursor.fetchone()['total']
        
        cursor.execute("""
            SELECT category, COUNT(*) as count FROM incidents
            WHERE created_at >= NOW() - INTERVAL '%s hours'
            GROUP BY category
            ORDER BY count DESC
        """, (hours,))
        by_category = cursor.fetchall()
        
        cursor.execute("""
            SELECT location, COUNT(*) as count FROM incidents
            WHERE created_at >= NOW() - INTERVAL '%s hours'
            GROUP BY location
            ORDER BY count DESC
            LIMIT 10
        """, (hours,))
        by_location = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            'total': total,
            'by_category': by_category,
            'by_location': by_location
        }
    except Exception as e:
        st.error(f"Error fetching statistics: {e}")
        return {}

def main():
    st.markdown("<h1 style='text-align: center;'>{} {}</h1>".format(
        DASHBOARD_CONFIG['icon'], DASHBOARD_CONFIG['title']
    ), unsafe_allow_html=True)
    
    st.markdown(
        "<p style='text-align: center; color: gray;'>Real-time monitoring of police, "
        "fire, rescue, and community incidents across Prince William County, Virginia</p>",
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        st.header("⚙️ Filters & Settings")
        
        time_range = st.selectbox(
            "Time Range",
            ["Last 1 Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days"],
            index=2
        )
        
        time_map = {
            "Last 1 Hour": 1,
            "Last 6 Hours": 6,
            "Last 24 Hours": 24,
            "Last 7 Days": 168
        }
        hours_back = time_map[time_range]
        
        categories = st.multiselect(
            "Incident Categories",
            list(INCIDENT_KEYWORDS.keys()),
            default=list(INCIDENT_KEYWORDS.keys())
        )
        
        locations = st.multiselect(
            "Locations",
            list(PWC_LOCATIONS.keys()),
            default=list(PWC_LOCATIONS.keys())
        )
        
        st.divider()
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📍 Map", "📰 Live Feed", "⚙️ Info"])
    
    with tab1:
        st.subheader("Statistics & Overview")
        
        stats = get_incident_stats(hours_back)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Incidents", stats.get('total', 0))
        
        with col2:
            police_count = sum([c['count'] for c in stats.get('by_category', []) if c['category'] == 'police'])
            st.metric("Police Incidents", police_count)
        
        with col3:
            fire_count = sum([c['count'] for c in stats.get('by_category', []) if c['category'] == 'fire'])
            st.metric("Fire/EMS Incidents", fire_count)
        
        with col4:
            rescue_count = sum([c['count'] for c in stats.get('by_category', []) if c['category'] == 'rescue'])
            st.metric("Rescue Incidents", rescue_count)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Incidents by Category")
            if stats.get('by_category'):
                category_df = pd.DataFrame(stats['by_category'])
                fig = px.pie(category_df, values='count', names='category')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Incidents by Location")
            if stats.get('by_location'):
                location_df = pd.DataFrame(stats['by_location'])
                fig = px.bar(location_df, x='location', y='count')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Incident Locations")
        
        incidents = get_recent_incidents(hours_back, 200)
        
        if not incidents.empty:
            m = folium.Map(
                location=[38.6240, -77.4458],
                zoom_start=10,
                tiles='OpenStreetMap'
            )
            
            for idx, incident in incidents.iterrows():
                if pd.notna(incident['latitude']) and pd.notna(incident['longitude']):
                    color = DASHBOARD_COLORS.get(incident.get('category', 'news'), 'blue')
                    
                    folium.CircleMarker(
                        location=[incident['latitude'], incident['longitude']],
                        radius=8,
                        popup=f"<b>{incident['title']}</b><br>{incident['location']}",
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.7
                    ).add_to(m)
            
            st_folium(m, width=1400, height=600)
        else:
            st.info("No incidents to display")
    
    with tab3:
        st.subheader("Live Incident Feed")
        
        incidents = get_recent_incidents(hours_back, 50)
        
        if not incidents.empty:
            for idx, incident in incidents.iterrows():
                col1, col2 = st.columns([0.15, 0.85])
                
                with col1:
                    category = incident.get('category', 'news')
                    color = DASHBOARD_COLORS.get(category, '#3498DB')
                    st.markdown(
                        f"<div style='background-color: {color}; padding: 10px; "
                        f"border-radius: 5px; text-align: center; color: white;'>"
                        f"{category.upper()}</div>",
                        unsafe_allow_html=True
                    )
                
                with col2:
                    st.markdown(f"**{incident['title']}**")
                    st.write(f"📍 {incident.get('location', 'Unknown')}")
                    st.write(f"⏰ {incident['created_at']}")
                
                st.divider()
        else:
            st.info("No incidents found")
    
    with tab4:
        st.subheader("About This Dashboard")
        st.info("""
        This OSINT dashboard monitors and aggregates incident data from:
        - Police Departments (Twitter)
        - Virginia Fire/EMS API
        - Local news RSS feeds
        - ArcGIS crime data
        - Community social media
        
        **For emergencies: Call 911**
        """)

if __name__ == "__main__":
    main()
