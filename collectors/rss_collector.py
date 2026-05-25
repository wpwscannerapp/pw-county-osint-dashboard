#!/usr/bin/env python3

import logging
import feedparser
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, RSS_FEEDS, INCIDENT_KEYWORDS, SCHEMA
from supabase import create_client, Client
from textblob import TextBlob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSCollector:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = f"{SCHEMA}.incidents"
        self.feeds = RSS_FEEDS
        self.keywords = INCIDENT_KEYWORDS

    def analyze_sentiment(self, text):
        try:
            return float(TextBlob(text).sentiment.polarity)
        except:
            return 0.0

    def check_keyword_match(self, text):
        text_lower = text.lower()
        matched = []
        for category, keywords in self.keywords.items():
            if any(kw in text_lower for kw in keywords):
                matched.append(category)
        return matched

    def store_incident(self, entry, feed_name, categories):
        try:
            sentiment = self.analyze_sentiment(entry.get('summary', entry.get('title', '')))
            category = categories[0] if categories else 'news'

            incident = {
                "title": entry.get('title', 'No Title'),
                "description": entry.get('summary', ''),
                "category": category,
                "source": feed_name,
                "source_url": entry.get('link', ''),
                "external_id": entry.get('id') or entry.get('link', ''),
                "sentiment": sentiment,
                "created_at": datetime.now().isoformat()
            }

            self.supabase.table(self.table_name).upsert(
                incident, 
                on_conflict="external_id"
            ).execute()

            logger.info(f"[+] Stored RSS: {entry.get('title')[:80]}...")
            return True

        except Exception as e:
            logger.error(f"[!] Store RSS failed: {e}")
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
            logger.info(f"[+] Collected {count} items from {feed_name}")
            return count
        except Exception as e:
            logger.error(f"[!] Feed error {feed_name}: {e}")
            return 0

    def collect_all(self):
        logger.info("[*] Starting RSS collection...")
        total = 0
        for feed in self.feeds:
            total += self.collect_from_feed(feed['url'], feed['name'])
        logger.info(f"[+] RSS collection complete. Total: {total}")


def run_rss_collector():
    RSSCollector().collect_all()


if __name__ == "__main__":
    run_rss_collector()
