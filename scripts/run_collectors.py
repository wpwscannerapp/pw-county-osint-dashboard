#!/usr/bin/env python3
"""
PWC OSINT Data Collectors - Direct Run Version
"""

import sys
import os

# Add current directory and parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Direct imports
import collectors.fire_ems_collector
import collectors.rss_collector
import collectors.facebook_collector

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 70)
    logger.info("🚀 Starting PWC OSINT Data Collectors")
    logger.info("=" * 70)

    try:
        logger.info("🔥 Running Fire & EMS Collector...")
        collectors.fire_ems_collector.run_fire_ems_collector()
        
        logger.info("📰 Running RSS/News Collector...")
        collectors.rss_collector.run_rss_collector()

        logger.info("📘 Running Facebook Collector...")
        collectors.facebook_collector.run_facebook_collector()

        logger.info("=" * 70)
        logger.info("✅ All collectors completed successfully!")
        logger.info("=" * 70)

    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
        raise

if __name__ == "__main__":
    main()
