#!/usr/bin/env python3

import logging
import requests
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, SCHEMA, FACEBOOK_PAGES
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacebookCollector:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = f"{SCHEMA}.incidents"
        self.pages = FACEBOOK_PAGES

    def store_incident(self, post):
        try:
            incident = {
                "title": post.get('title', 'Facebook Post'),
                "description": post.get('message', ''),
                "category": post.get('category', 'news'),
                "source": post.get('source'),
                "source_url": post.get('url', ''),
                "external_id": post.get('post_id'),
                "created_at": post.get('created_time', datetime.now().isoformat())
            }

            self.supabase.table(self.table_name).upsert(
                incident, on_conflict="external_id"
            ).execute()

            logger.info(f"[+] Stored Facebook post: {incident['title'][:80]}...")
            return True
        except Exception as e:
            logger.error(f"[!] Store Facebook failed: {e}")
            return False

    def collect_from_page(self, page):
        logger.info(f"[*] Collecting from Facebook: {page['name']}")
        # Note: Real Facebook scraping is restricted. This is a placeholder.
        # For production, consider using Facebook Graph API with proper access token.
        try:
            # Placeholder logic - replace with actual scraping or API call
            logger.info(f"   → Would fetch posts from {page['url']}")
            # Example dummy post for testing:
            dummy_post = {
                "title": f"Update from {page['name']}",
                "message": "Sample incident post from Western Prince William Scanner Feed",
                "category": "news",
                "source": page['name'],
                "url": page['url'],
                "post_id": f"fb_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "created_time": datetime.now().isoformat()
            }
            self.store_incident(dummy_post)
        except Exception as e:
            logger.error(f"Facebook collection error: {e}")

    def collect_all(self):
        logger.info("[*] Starting Facebook collection...")
        for page in self.pages:
            self.collect_from_page(page)


def run_facebook_collector():
    FacebookCollector().collect_all()


if __name__ == "__main__":
    run_facebook_collector()
