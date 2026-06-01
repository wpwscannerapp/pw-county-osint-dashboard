import os
from dotenv import load_dotenv

load_dotenv()

# ========================
# DATABASE (Neon)
# ========================
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL environment variable is required")

SCHEMA = "pwc_osint"

# ========================
# Facebook & X Config
# ========================
FACEBOOK_PAGES = [
    {"name": "Prince William County Police", "url": "https://facebook.com/PWCPD"},
    {"name": "Western Prince William Scanner", "url": "https://facebook.com/WesternPrinceWilliamScanner"},
]

X_ACCOUNTS = [
    "PWCPD",
    "ManassasCityPD",
    "PWCountyGov"
]

X_KEYWORDS = ["incident", "crash", "fire", "police", "rescue", "shooting", "emergency"]

# ========================
# Other configs (Locations, RSS, Keywords)
# ========================
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

RSS_FEEDS = [
    {"name": "Potomac Local News", "url": "https://potomaclocal.com/feed/"},
    {"name": "Prince William Living", "url": "https://princewilliamliving.com/feed/"},
    {"name": "Bristow Beat", "url": "https://bristowbeat.com/feed/"},
]

INCIDENT_KEYWORDS = {
    'police': ['police', 'shooting', 'arrest', 'crime', 'officer'],
    'fire': ['fire', 'burning', 'explosion'],
    'rescue': ['rescue', 'medical', 'ambulance'],
    'traffic': ['crash', 'accident', 'traffic']
}
