#!/usr/bin/env python3
"""
Main runner for all PWC OSINT Collectors
"""
import logging
from collectors.fire_ems_collector import run_fire_ems_collector
from collectors.rss_collector import run_rss_collector
from collectors.facebook_collector import run_facebook_collector
from collectors.x_collector import run_x_collector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 70)
    logger.info("🚀 STARTING ALL PWC OSINT DATA COLLECTORS")
    logger.info("=" * 70)

    try:
        run_fire_ems_collector()
        run_rss_collector()
        run_facebook_collector()
        run_x_collector()

        logger.info("=" * 70)
        logger.info("✅ ALL COLLECTORS FINISHED SUCCESSFULLY")
        logger.info("=" * 70)

    except Exception as e:
        logger.error(f"❌ Critical error running collectors: {e}")

if __name__ == "__main__":
    main()
