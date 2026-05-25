import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")

SCHEMA = "pwc_osint"

# === Your configurations ===
PWC_LOCATIONS = { ... }   # Keep your existing locations

RSS_FEEDS = [
    {"name": "Potomac Local News", "url": "https://potomaclocal.com/feed/"},
    {"name": "Prince William Living", "url": "https://princewilliamliving.com/feed/"},
    {"name": "Bristow Beat", "url": "https://bristowbeat.com/feed/"},
]

INCIDENT_KEYWORDS = { ... }  # Keep your existing keywords
