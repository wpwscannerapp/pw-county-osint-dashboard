#!/usr/bin/env python3

import logging
import feedparser
from datetime import datetime
from config import RSS_FEEDS, INCIDENT_KEYWORDS, DATABASE_URL
import psycopg2
from textblob import TextBlob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSSCollector:
    def __init__(self):
        self.db_url = DATABASE_URL
        self.feeds = RSS_FEEDS
        self.keywords = INCIDENT_KEYWORDS
        self.conn = None
    
    def connect_db(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            logger.info("[+] Connected to database")
        except Exception as e:
            logger.error(f"[!] Database connection failed: {e}")
            raise
    
    def close_db(self):
        if self.conn:
            self.conn.close()
            logger.info("[+] Database connection closed")
    
    def analyze_sentiment(self, text):
        try:
            blob = TextBlob(text)
            return float(blob.sentiment.polarity)
        except:
            return 0.0
    
    def check_keyword_match(self, text):
        text_lower = text.lower()
        matched_categories = []
        
        for category, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    matched_categories.append(category)
                    break
        
        return matched_categories
    
    def store_incident(self, entry, feed_name, categories):
        try:
            cursor = self.conn.cursor()
            
            query = """
                INSERT INTO incidents 
                (title, description, category, source, source_url, 
                 external_id, sentiment, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (external_id) DO NOTHING
            """
            
            sentiment = self.analyze_sentiment(
                entry.get('summary', entry.get('title', ''))
            )
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
            logger.info(f"[+] Stored RSS entry: {entry.get('title', 'Unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"[!] Error storing RSS entry: {e}")
            return False
    
    def collect_from_feed(self, feed_url, feed_name):
        logger.info(f"[*] Collecting from {feed_name}...")
        
        try:
            feed = feedparser.parse(feed_url)
            
            if feed.status != 200:
                logger.warning(f"[!] Feed returned status {feed.status}: {feed_url}")
                return 0
            
            count = 0
            for entry in feed.entries[:10]:
                categories = self.check_keyword_match(
                    entry.get('title', '') + " " + entry.get('summary', '')
                )
                
                if self.store_incident(entry, feed_name, categories):
                    count += 1
            
            logger.info(f"[+] Collected {count} entries from {feed_name}")
            return count
            
        except Exception as e:
            logger.error(f"[!] Error collecting from {feed_name}: {e}")
            return 0
    
    def collect_all(self):
        logger.info("[*] Starting RSS data collection...")
        
        self.connect_db()
        
        try:
            total = 0
            for feed in self.feeds:
                count = self.collect_from_feed(feed['url'], feed['name'])
                total += count
            
            logger.info(f"[+] RSS data collection complete. Total entries: {total}")
            
        finally:
            self.close_db()

def run_rss_collector():
    collector = RSSCollector()
    collector.collect_all()

if __name__ == "__main__":
    run_rss_collector()
