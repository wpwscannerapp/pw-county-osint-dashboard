#!/usr/bin/env python3
"""
X/Twitter Collector for PWC OSINT Dashboard
Monitors official and local accounts for real-time alerts
"""

import logging
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, SCHEMA, X_ACCOUNTS, X_KEYWORDS
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import snscrape (common for scraping)
try:
    import snscrape.modules.twitter as sntwitter
except ImportError:
    sntwitter = None
    logger.warning("snscrape not installed. Install with: pip install snscrape")


class XCollector:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = f"{SCHEMA}.incidents"
        self.accounts = X_ACCOUNTS
        self.keywords = X_KEYWORDS

    def store_incident(self, tweet):
        try:
            incident = {
                "title": tweet.content[:250],
                "description": tweet.content,
                "category": "police",  # Can be improved with better classification
                "incident_type": "social-media-alert",
                "location": "Prince William County",
                "source": f"X/@{tweet.user.username}",
                "source_url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}",
                "external_id": str(tweet.id),
                "created_at": tweet.date.isoformat() if hasattr(tweet, 'date') else datetime.now().isoformat()
            }

            self.supabase.table(self.table_name).upsert(
                incident,
                on_conflict="external_id"
            ).execute()

            logger.info(f"[+] Stored X post from @{tweet.user.username}")
            return True
        except Exception as e:
            logger.error(f"[!] Failed to store X post: {e}")
            return False

    def collect_from_account(self, username):
        if not sntwitter:
            logger.warning(f"snscrape not available for @{username}")
            return 0

        logger.info(f"[*] Collecting recent tweets from @{username}...")
        try:
            count = 0
            # Search recent tweets from this account
            query = f"from:{username} since:2026-05-01"

            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                text = tweet.content.lower()
                
                # Only store if it matches keywords
                if any(kw in text for kw in self.keywords):
                    if self.store_incident(tweet):
                        count += 1
                
                if count >= 15:  # Limit per account per run
                    break

            logger.info(f"[+] Collected {count} relevant posts from @{username}")
            return count

        except Exception as e:
            logger.error(f"Error collecting from @{username}: {e}")
            return 0

    def collect_all(self):
        logger.info("[*] Starting X/Twitter collection...")
        total = 0
        for account
