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

# New: Schema name for Supabase
SCHEMA = "pwc_osint"

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
        'lat': 38.6546,
        'lon': -77.4280,
        'radius_miles': 20,
        'type': 'county'
    }
}

# ========================
# RSS FEEDS (Add more as needed)
# ========================
RSS_FEEDS = [
    {"name": "Potomac Local News", "url": "https://potomaclocal.com/feed/"},
    {"name": "Prince William Living", "url": "https://princewilliamliving.com/feed/"},
    {"name": "Bristow Beat", "url": "https://bristowbeat.com/feed/"},
    # Add more feeds here
]

# ========================
# INCIDENT KEYWORDS
# ========================
INCIDENT_KEYWORDS = {
    'police': ['police', 'shooting', 'arrest', 'crime', 'officer', 'sheriff'],
    'fire': ['fire', 'burning', 'explosion', 'smoke'],
    'rescue': ['rescue', 'medical', 'ambulance', 'ems', 'injury'],
    'traffic': ['crash', 'accident', 'traffic', 'road closed']
}
