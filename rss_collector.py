#!/usr/bin/env python3
import logging
import feedparser
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, RSS_FEEDS, INCIDENT_KEYWORDS
from supabase import create_client, Client
from textblob import TextBlob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSCollector:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = "pwc_osint.incidents"   # Hardcoded
        self.feeds = RSS_FEEDS
        self.keywords = INCIDENT_KEYWORDS

    def analyze_sentiment(self, text):
        try:
            return float(TextBlob(text).sentiment.polarity)
        except:
            return 0.0

    def check_keyword_match(self, text):
        text_lower = text.lower()
        return [cat for cat, kws in self.keywords.items() if any(kw in text_lower for kw in kws)]

    def store_incident(self, entry, feed_name, categories):
        try:
            incident = {
                "title": entry.get('title', 'No Title'),
                "description": entry.get('summary', ''),
                "category": categories[0] if categories else 'news',
                "source": feed_name,
                "source_url": entry.get('link', ''),
                "external_id": entry.get('id') or entry.get('link', ''),
                "sentiment": self.analyze_sentiment(entry.get('summary', entry.get('title', ''))),
                "created_at": datetime.now().isoformat()
            }
            self.supabase.table(self.table_name).upsert(incident, on_conflict="external_id").execute()
            logger.info(f"[+] Stored RSS: {entry.get('title')[:80]}...")
            return True
        except Exception as e:
            logger.error(f"[!] Store failed: {e}")
            return False

    def collect_from_feed(self, feed_url, feed_name):
        logger.info(f"[*] Collecting from {feed_name}...")
        try:
            feed = feedparser.parse(feed_url)
            count = 0
            for entry in feed.entries[:15]:
                text = entry.get('title', '') + " " + entry.get('summary', '')
                categories = self.check_keyword_match(text)
                if categories and self.store_incident(entry, feed_name, categories):
                    count += 1
            logger.info(f"[+] Collected {count} from {feed_name}")
            return count
        except Exception as e:
            logger.error(f"[!] Feed error: {e}")
            return 0

    def collect_all(self):
        logger.info("[*] Starting RSS collection...")
        total = sum(self.collect_from_feed(feed['url'], feed['name']) for feed in self.feeds)
        logger.info(f"[+] RSS total: {total}")

def run_rss_collector():
    RSSCollector().collect_all()

if __name__ == "__main__":
    run_rss_collector()
