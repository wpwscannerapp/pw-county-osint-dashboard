#!/usr/bin/env python3
import logging
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, SCHEMA, FACEBOOK_PAGES
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacebookCollector:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = "pwc_osint.incidents"   # Hardcoded

    def store_incident(self, post):
        try:
            incident = {
                "title": post.get("title", "Facebook Update"),
                "description": post.get("message", ""),
                "category": post.get("category", "news"),
                "source": post.get("source"),
                "source_url": post.get("url", ""),
                "external_id": post.get("post_id"),
                "created_at": datetime.now().isoformat()
            }
            self.supabase.table(self.table_name).upsert(incident, on_conflict="external_id").execute()
            logger.info(f"[+] Stored Facebook post")
            return True
        except Exception as e:
            logger.error(f"[!] Store failed: {e}")
            return False

    def collect_all(self):
        logger.info("[*] Starting Facebook collection...")
        for page in FACEBOOK_PAGES:
            logger.info(f"   → Scanning {page['name']}")
            # Placeholder for now (real implementation later)
            dummy = {
                "title": f"Update from {page['name']}",
                "message": "Sample post from Western Prince William Scanner Feed",
                "category": "news",
                "source": page['name'],
                "url": page['url'],
                "post_id": f"fb_{int(datetime.now().timestamp())}"
            }
            self.store_incident(dummy)

def run_facebook_collector():
    FacebookCollector().collect_all()

if __name__ == "__main__":
    run_facebook_collector()
