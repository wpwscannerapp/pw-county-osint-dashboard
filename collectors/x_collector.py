#!/usr/bin/env python3
import logging
from datetime import datetime
from config import DATABASE_URL, SCHEMA, X_ACCOUNTS, X_KEYWORDS
import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XCollector:
    def __init__(self):
        self.db_url = DATABASE_URL
        self.schema = SCHEMA
        self.accounts = X_ACCOUNTS
        self.keywords = X_KEYWORDS
        self.conn = None

    def connect_db(self):
        self.conn = psycopg2.connect(self.db_url, connect_timeout=10)
        logger.info("[+] Connected to Neon")

    def close_db(self):
        if self.conn:
            self.conn.close()

    def store_incident(self, tweet):
        try:
            cursor = self.conn.cursor()
            query = f"""
                INSERT INTO {self.schema}.incidents
                (title, description, category, source, source_url, external_id, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (external_id) DO NOTHING
            """
            cursor.execute(query, (
                tweet.get('title', 'X Post'),
                tweet.get('text', ''),
                tweet.get('category', 'news'),
                'X (Twitter)',
                tweet.get('url', ''),
                tweet.get('id', ''),
                datetime.now()
            ))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"[!] Store X error: {e}")
            return False

    def collect_all(self):
        logger.info("[*] X/Twitter collector started (placeholder)")
        self.connect_db()
        try:
            # TODO: Add actual X API or scraping logic
            logger.info("[+] X collection complete (placeholder)")
        finally:
            self.close_db()

def run_x_collector():
    XCollector().collect_all()

if __name__ == "__main__":
    run_x_collector()
