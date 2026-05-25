#!/usr/bin/env python3
"""
Main script to run all data collectors for PWC OSINT Dashboard
"""
import logging
from collectors.fire_ems_collector import run_fire_ems_collector
from collectors.rss_collector import run_rss_collector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 60)
    logger.info("🚀 Starting PWC OSINT Data Collectors")
    logger.info("=" * 60)

    try:
        # Run Fire/EMS Collector
        logger.info("🔥 Running Fire & EMS Collector...")
        run_fire_ems_collector()
        
        # Run RSS/News Collector
        logger.info("📰 Running RSS/News Collector...")
        run_rss_collector()

        logger.info("=" * 60)
        logger.info("✅ All collectors completed successfully!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Error running collectors: {e}")
        raise

if __name__ == "__main__":
    main()
