#!/usr/bin/env python3
"""
PWC OSINT Dashboard - Main Collectors Runner
Runs all data sources: Fire/EMS, RSS, Facebook, and X/Twitter
"""

import logging
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collectors.fire_ems_collector import run_fire_ems_collector
from collectors.rss_collector import run_rss_collector
from collectors.facebook_collector import run_facebook_collector
from collectors.x_collector import run_x_collector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 80)
    logger.info("🚀 PWC OSINT DATA COLLECTORS STARTED")
    logger.info("=" * 80)

    try:
        # Fire/EMS Collector
        logger.info("🔥 Running Fire & EMS Collector...")
        run_fire_ems_collector()

        # RSS/News Collector
        logger.info("📰 Running RSS/News Collector...")
        run_rss_collector()

        # Facebook Collector
        logger.info("📘 Running Facebook Collector...")
        run_facebook_collector()

        # X/Twitter Collector
        logger.info("🐦 Running X/Twitter Collector...")
        run_x_collector()

        logger.info("=" * 80)
        logger.info("✅ ALL COLLECTORS COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"❌ Critical error in collectors: {e}")
        raise


if __name__ == "__main__":
    main()
