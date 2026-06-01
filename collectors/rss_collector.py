#!/usr/bin/env python3
import logging
import feedparser
from datetime import datetime
from config import RSS_FEEDS, INCIDENT_KEYWORDS, DATABASE_URL, SCHEMA
import psycopg2
from textblob import TextBlob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSSCollector:
    def __init__(self):
        self.db_url = DATABASE_URL
        self.schema = SCHEMA
        self.feeds = RSS_FEEDS
        self.keywords = INCIDENT_KEYWORDS
        self.conn = None
   
    def connect_db(self):
        try:
            self.conn = psycopg2.connect(self.db_url, connect_timeout=10)
            logger.info("[+] Connected to Neon")
        except Exception as e:
            logger.error(f"[!] Database connection failed: {e}")
            raise
   
    def close_db(self):
        if self.conn:
            self.conn.close()
   
    def analyze_sentiment(self, text):
        try:
            blob = TextBlob(text)
            return float(blob.sentiment.polarity)
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
            cursor = self.conn.cursor()
            query = f"""
                INSERT INTO {self.schema}.incidents
                (title, description, category, source, source_url, external_id, sentiment, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (external_id) DO NOTHING
            """
            sentiment = self.analyze_sentiment(entry.get('summary', entry.get('title', '')))
            category = categories[0] if categories else 'news'

            cursor.execute(query, (
                entry.get('title', 'No Title'),
                entry.get('summary', ''),
                category,
                feed_name,
                entry.get('link', ''),
                entry.get('id', entry.get('link', '')),
                sentiment,
                datetime.now()
            ))
            self.conn.commit()
            cursor.close()
            logger.info(f"[+] Stored RSS: {entry.get('title')[:60]}...")
            return True
        except Exception as e:
            logger.error(f"[!] Store RSS error: {e}")
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
            logger.info(f"[+] Collected {count} entries from {feed_name}")
            return count
        except Exception as e:
            logger.error(f"[!] Feed error {feed_name}: {e}")
            return 0

    def collect_all(self):
        logger.info("[*] Starting RSS data collection...")
        self.connect_db()
        try:
            total = 0
            for feed in self.feeds:
                total += self.collect_from_feed(feed['url'], feed['name'])
            logger.info(f"[+] RSS collection complete. Total: {total}")
        finally:
            self.close_db()

def run_rss_collector():
    RSSCollector().collect_all()

if __name__ == "__main__":
    run_rss_collector()
