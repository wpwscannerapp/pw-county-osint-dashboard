#!/usr/bin/env python3
import logging
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, SCHEMA, X_ACCOUNTS, X_KEYWORDS
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Note: snscrape is easy but being phased out. For production, consider twscrape or official API.
try:
    import snscrape.modules.twitter as sntwitter
except ImportError:
    logger.error("snscrape not installed. Run: pip install snscrape")
    sntwitter = None


class XCollector:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = f"{SCHEMA}.incidents"
        self.accounts = X_ACCOUNTS
        self.keywords = X_KEYWORDS

    def store_incident(self, tweet):
        try:
            incident = {
                "title": tweet.content[:200],
                "description": tweet.content,
                "category": "police",  # You can improve categorization logic
                "source": f"X/@{tweet.user.username}",
                "source_url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}",
                "external_id": str(tweet.id),
                "created_at": tweet.date.isoformat()
            }

            self.supabase.table(self.table_name).upsert(
                incident, on_conflict="external_id"
            ).execute()

            logger.info(f"[+] Stored X post from @{tweet.user.username}")
            return True
        except Exception as e:
            logger.error(f"[!] Store X failed: {e}")
            return False

    def collect_from_account(self, username):
        logger.info(f"[*] Collecting from X/@{username}...")
        if not sntwitter:
            logger.warning("snscrape not available")
            return 0

        try:
            count = 0
            query = f"from:{username} since:2026-05-01"  # Adjust date as needed

            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                if any(kw in tweet.content.lower() for kw in self.keywords):
                    if self.store_incident(tweet):
                        count += 1
                if count >= 20:  # Limit per run
                    break

            logger.info(f"[+] Collected {count} relevant posts from @{username}")
            return count
        except Exception as e:
            logger.error(f"X collection error for @{username}: {e}")
            return 0

    def collect_all(self):
        logger.info("[*] Starting X/Twitter collection...")
        total = 0
        for account in self.accounts:
            total += self.collect_from_account(account)
        logger.info(f"[+] X collection finished. Total: {total}")


def run_x_collector():
    XCollector().collect_all()


if __name__ == "__main__":
    run_x_collector()
