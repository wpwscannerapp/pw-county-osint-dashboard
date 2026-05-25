import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")

SCHEMA = "pwc_osint"

# === Locations ===
PWC_LOCATIONS = {
    'Manassas': {'lat': 38.7509, 'lon': -77.4734, 'radius_miles': 5},
    'Manassas Park': {'lat': 38.7942, 'lon': -77.4521, 'radius_miles': 3},
    'Woodbridge': {'lat': 38.6255, 'lon': -77.2636, 'radius_miles': 8},
    'Haymarket': {'lat': 38.6431, 'lon': -77.6314, 'radius_miles': 4},
    'Triangle': {'lat': 38.6147, 'lon': -77.3264, 'radius_miles': 3},
    'Dumfries': {'lat': 38.5697, 'lon': -77.3042, 'radius_miles': 5},
    'Occoquan': {'lat': 38.6835, 'lon': -77.2825, 'radius_miles': 2},
    'Prince William County': {'lat': 38.6546, 'lon': -77.4280, 'radius_miles': 20},
}

# === RSS Feeds ===
RSS_FEEDS = [
    {"name": "Potomac Local News", "url": "https://potomaclocal.com/feed/"},
    {"name": "Prince William Living", "url": "https://princewilliamliving.com/feed/"},
    {"name": "Bristow Beat", "url": "https://bristowbeat.com/feed/"},
]

# === Facebook Pages ===
FACEBOOK_PAGES = [
    {
        "name": "Western Prince William Scanner Feed",
        "url": "https://www.facebook.com/WesternPrinceWilliamScannerFeed",   # Update if needed
        "page_id": ""  # Optional: if you have the numeric ID
    }
]

# === Keywords ===
INCIDENT_KEYWORDS = {
    'police': ['police', 'shooting', 'arrest', 'crime', 'officer', 'sheriff'],
    'fire': ['fire', 'burning', 'explosion', 'smoke'],
    'rescue': ['rescue', 'ambulance', 'ems', 'medical', 'injury'],
    'traffic': ['crash', 'accident', 'traffic', 'road closed'],
}
