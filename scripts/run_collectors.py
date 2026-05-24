#!/usr/bin/env python3

import logging
import time
from datetime import datetime
from collectors.rss_collector import RSSCollector
from collectors.fire_ems_collector import FireEMSCollector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_all_collectors():
    """Run all data collectors in sequence"""
    logger.info("="*60)
    logger.info(f"Starting data collection cycle at {datetime.now()}")
    logger.info("="*60)
    
    start_time = time.time()
    
    try:
        logger.info("\n[1/2] Running RSS Feed Collector...")
        rss_collector = RSSCollector()
        rss_collector.collect_all()
        
        logger.info("\n[2/2] Running Fire/EMS Data Collector...")
        fire_ems_collector = FireEMSCollector()
        fire_ems_collector.collect_all()
        
    except Exception as e:
        logger.error(f"[!] Error during data collection: {e}")
        raise
    finally:
        elapsed_time = time.time() - start_time
        logger.info("="*60)
        logger.info(f"Data collection cycle complete")
        logger.info(f"Elapsed time: {elapsed_time:.2f} seconds")
        logger.info("="*60)

if __name__ == "__main__":
    run_all_collectors()
