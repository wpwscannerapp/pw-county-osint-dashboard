import os
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials (use public Anon key for collectors)
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")

SCHEMA = "pwc_osint"

# Keep your existing location and RSS config
PWC_LOCATIONS = { ... }   # (keep your current dictionary)
RSS_FEEDS = [ ... ]       # (keep your current feeds)
INCIDENT_KEYWORDS = { ... }  # (keep your current keywords)
