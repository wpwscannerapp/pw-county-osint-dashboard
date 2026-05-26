#!/usr/bin/env python3
"""
Simple PWC OSINT Collectors Runner
"""

import logging
from fire_ems_collector import run_fire_ems_collector
from rss_collector import run_rss_collector
from facebook_collector import run_facebook_collector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 70)
    logger.info("🚀 Starting PWC OSINT Data Collectors")
    logger.info("=" * 70)

    run_fire_ems_collector()
    run_rss_collector()
    run_facebook_collector()

    logger.info("=" * 70)
    logger.info("✅ All collectors finished!")
    logger.info("=" * 70)

if __name__ == "__main__":
    main()
