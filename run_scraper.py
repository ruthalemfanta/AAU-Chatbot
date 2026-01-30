import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from web_scrapper import run_periodic_scraping
import schedule
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'once'
    
    if mode == 'continuous':
        logger.info("Starting continuous scraping mode - runs every 24 hours")
        
        run_periodic_scraping()
        
        schedule.every(24).hours.do(run_periodic_scraping)
        
        while True:
            schedule.run_pending()
            time.sleep(3600)
    else:
        logger.info("Running scraper once")
        run_periodic_scraping()
