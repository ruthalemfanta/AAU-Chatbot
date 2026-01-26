"""Combined data collection script for web scraping and Telegram."""
import sys
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_web_scraping():
    """Run web scraping collection."""
    logger.info("=" * 60)
    logger.info("Starting Web Scraping Collection")
    logger.info("=" * 60)
    
    try:
        from scripts.web_scrapper import AAUWebScraper, get_aau_target_urls
        
        scraper = AAUWebScraper()
        target_urls = get_aau_target_urls()
        
        logger.info(f"Scraping {sum(len(urls) for urls in target_urls.values())} pages...")
        
        collected_data = scraper.scrape_target_pages(target_urls)
        
        output_path = Path("data/raw/collected_data.csv")
        scraper.save_to_csv(collected_data, output_path)
        
        logger.info(f"Web scraping complete! Collected {len(collected_data)} Q&A pairs")
        return len(collected_data)
    except Exception as e:
        logger.error(f"Web scraping failed: {e}")
        return 0


def run_telegram_collection(api_token=None):
    """Run Telegram collection."""
    logger.info("=" * 60)
    logger.info("Starting Telegram Collection")
    logger.info("=" * 60)
    
    try:
        from scripts.telegram_cli import TelegramDataCollector, collect_from_telegram_api
        
        AAU_TELEGRAM_CHANNELS = [
            "https://t.me/aau_official",
            "https://t.me/CTBEAAU",
            "https://t.me/SchoolofCommerceocs",
            "https://t.me/aausc_1943"
        ]
        
        collector = TelegramDataCollector()
        
        logger.info("Channels to collect from:")
        for channel in AAU_TELEGRAM_CHANNELS:
            logger.info(f"  - {channel}")
        
        if api_token:
            logger.info("Using provided API token for Telegram collection...")
            channel_usernames = [ch.replace('https://t.me/', '') for ch in AAU_TELEGRAM_CHANNELS]
            collect_from_telegram_api(api_token, channel_usernames)
            collector.save_to_csv("data/raw/collected_data.csv", append=True)
            logger.info(f"Telegram collection complete! Collected {len(collector.collected_data)} messages")
            return len(collector.collected_data)
        else:
            logger.warning("No Telegram API token provided. Skipping Telegram collection.")
            logger.info("To collect from Telegram, set TELEGRAM_API_TOKEN environment variable")
            logger.info("or provide it as command line argument: python scripts/collect_data.py <token>")
            return 0
    except Exception as e:
        logger.error(f"Telegram collection failed: {e}")
        return 0


def main():
    """Main function to run both collection methods."""
    logger.info("AAU Data Collection - Starting Combined Collection")
    logger.info("=" * 60)
    
    api_token = None
    if len(sys.argv) > 1:
        api_token = sys.argv[1]
    elif os.getenv('TELEGRAM_API_TOKEN'):
        api_token = os.getenv('TELEGRAM_API_TOKEN')
    
    web_count = run_web_scraping()
    telegram_count = run_telegram_collection(api_token)
    
    total = web_count + telegram_count
    
    logger.info("=" * 60)
    logger.info("Collection Summary")
    logger.info("=" * 60)
    logger.info(f"Web scraping: {web_count} items")
    logger.info(f"Telegram: {telegram_count} items")
    logger.info(f"Total collected: {total} items")
    logger.info(f"Data saved to: data/raw/collected_data.csv")
    
    if total > 0:
        logger.info("\nNext steps:")
        logger.info("1. Process data: python -m app.data_processor")
        logger.info("2. Generate statistics: python scripts/data_stats.py")
    else:
        logger.warning("No data collected. Check errors above.")


if __name__ == "__main__":
    main()
