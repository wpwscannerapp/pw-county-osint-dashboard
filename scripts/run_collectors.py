#!/usr/bin/env python3
"""
PWC OSINT Data Collectors Runner
"""

import sys
import os

# Force add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

print(f"Project root added to path: {project_root}")  # Debug line

# Now import the collectors
from collectors.fire_ems_collector import run_fire_ems_collector
from collectors.rss_collector import run_rss_collector
from collectors.facebook_collector import run_facebook_collector

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
        run_fire_ems_collector()
        
        logger.info("📰 Running RSS/News Collector...")
        run_rss_collector()

        logger.info("📘 Running Facebook Collector...")
        run_facebook_collector()

        logger.info("=" * 70)
        logger.info("✅ All collectors completed successfully!")
        logger.info("=" * 70)

    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
        raise

if __name__ == "__main__":
    main()
