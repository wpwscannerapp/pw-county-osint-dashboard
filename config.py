import os
from dotenv import load_dotenv

load_dotenv()

# ========================
# DATABASE CONFIGURATION
# ========================
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://pwc_osint:secure_password@localhost/pwc_osint_db'
)

# ========================
# LOCATION CONFIGURATION
# ========================
PWC_LOCATIONS = {
    'Manassas': {
        'lat': 38.7509,
        'lon': -77.4734,
        'radius_miles': 5,
        'type': 'city'
    },
    'Manassas Park': {
        'lat': 38.7942,
        'lon': -77.4521,
        'radius_miles': 3,
        'type': 'city'
    },
    'Woodbridge': {
        'lat': 38.6255,
        'lon': -77.2636,
        'radius_miles': 8,
        'type': 'town'
    },
    'Haymarket': {
        'lat': 38.6431,
        'lon': -77.6314,
        'radius_miles': 4,
        'type': 'town'
    },
    'Triangle': {
        'lat': 38.6147,
        'lon': -77.3264,
        'radius_miles': 3,
        'type': 'town'
    },
    'Dumfries': {
        'lat': 38.5697,
        'lon': -77.3042,
        'radius_miles': 5,
        'type': 'town'
    },
    'Occoquan': {
        'lat': 38.6835,
        'lon': -77.2825,
        'radius_miles': 2,
        'type': 'town'
    },
    'Prince William County': {
        'lat': 38.6240,
        'lon': -77.4458,
        'radius_miles': 25,
        'type': 'county'
    }
}

# ========================
# TWITTER/X CONFIGURATION
# ========================
TWITTER_ACCOUNTS_TO_MONITOR = [
    {
        'handle': '@PWCPD',
        'name': 'Prince William County Police',
        'category': 'police'
    },
    {
        'handle': '@ManassasCityPD',
        'name': 'Manassas City Police',
        'category': 'police'
    },
    {
        'handle': '@PotomacLocal',
        'name': 'Potomac Local News',
        'category': 'news'
    },
    {
        'handle': '@BristowBeat',
        'name': 'Bristow Beat',
        'category': 'news'
    },
]

# Keywords for incident detection
INCIDENT_KEYWORDS = {
    'police': ['police', 'arrest', 'warrant', 'suspect', 'charged', 'felony'],
    'fire': ['fire', 'structure fire', 'house fire', 'vehicle fire'],
    'rescue': ['rescue', 'emergency', 'ems', 'ambulance', 'medical'],
    'accident': ['accident', 'crash', 'collision', 'mva', 'traffic'],
    'crime': ['shooting', 'robbery', 'theft', 'burglary', 'assault'],
    'emergency': ['emergency', 'incident', 'hazmat', 'evacuation']
}

# ========================
# RSS FEED CONFIGURATION
# ========================
RSS_FEEDS = [
    {
        'url': 'https://www.potomaclocal.com/feed/',
        'name': 'Potomac Local News',
        'category': 'news'
    },
    {
        'url': 'https://www.bristowbeat.com/feed/',
        'name': 'Bristow Beat',
        'category': 'news'
    },
    {
        'url': 'https://princewilliamliving.com/feed/',
        'name': 'Prince William Living',
        'category': 'news'
    },
    {
        'url': 'https://wtop.com/local/prince-william-county/feed/',
        'name': 'WTOP - Prince William County',
        'category': 'news'
    },
]

# ========================
# DATA COLLECTION SCHEDULE
# ========================
COLLECTION_SCHEDULES = {
    'twitter': {'minutes': 2},
    'rss': {'minutes': 10},
    'fire_ems_api': {'minutes': 5},
    'arcgis_crime': {'minutes': 30},
}

# ========================
# STREAMLIT DASHBOARD CONFIG
# ========================
DASHBOARD_CONFIG = {
    'title': 'Prince William County OSINT Dashboard',
    'icon': '🚨',
    'layout': 'wide',
    'page_title': 'PWC Emergency Monitor',
}

DASHBOARD_COLORS = {
    'police': '#FF6B6B',
    'fire': '#FFA500',
    'rescue': '#4ECDC4',
    'accident': '#FFD93D',
    'crime': '#CC0000',
    'emergency': '#9B59B6',
    'news': '#3498DB',
}

# ========================
# ALERT CONFIGURATION
# ========================
ALERT_CONFIG = {
    'enabled': True,
    'high_priority_keywords': ['shooting', 'robbery', 'armed', 'explosion'],
    'alert_cooldown_minutes': 15
}

# ========================
# FEATURES
# ========================
FEATURES = {
    'twitter_monitoring': True,
    'rss_feeds': True,
    'fire_ems_api': True,
    'sentiment_analysis': True,
    'incident_mapping': True,
    'alerts': True,
}
