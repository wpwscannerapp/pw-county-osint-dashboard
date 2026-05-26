#!/usr/bin/env python3
"""
PWC OSINT Dashboard - Main Collectors Runner
Runs Fire/EMS, RSS, Facebook, and X/Twitter collectors
"""

import logging
import sys
import os

# Ensure we can import from collectors
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collectors.fire_ems_collector import run_fire_ems_collector
from collectors.rss_collector import run_rss_collector
from collectors.facebook_collector import run_facebook_collector
from collectors.x_collector import run_x_collector   # Optional for now

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 80)
    logger.info("🚀 STARTING PWC OSINT DATA COLLECTORS")
    logger.info("=" * 80)

    try:
        logger.info("🔥 Running Fire & EMS Collector...")
        run_fire_ems_collector()

        logger.info("📰 Running RSS/News Collector...")
        run_rss_collector()

        logger.info("📘 Running Facebook Collector...")
        run_facebook_collector()

        # Optional: X/Twitter Collector
        # logger.info("🐦 Running X/Twitter Collector...")
        # run_x_collector()

        logger.info("=" * 80)
        logger.info("✅ ALL COLLECTORS COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
        raise


if __name__ == "__main__":
    main()
