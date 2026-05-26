#!/usr/bin/env python3
import logging
from collectors.fire_ems_collector import run_fire_ems_collector
from collectors.rss_collector import run_rss_collector
from collectors.facebook_collector import run_facebook_collector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 70)
    logger.info("🚀 PWC OSINT Data Collectors Started")
    logger.info("=" * 70)

    run_fire_ems_collector()
    run_rss_collector()
    run_facebook_collector()

    logger.info("=" * 70)
    logger.info("✅ All collectors finished successfully!")
    logger.info("=" * 70)

if __name__ == "__main__":
    main()
