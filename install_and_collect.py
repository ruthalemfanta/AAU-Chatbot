"""Install dependencies and run data collection."""
import subprocess
import sys
from pathlib import Path

def install_package(package):
    """Install a Python package."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 70)
    print("Installing Dependencies and Running Data Collection")
    print("=" * 70)
    
    print("\n[1/3] Installing python-telegram-bot...")
    if install_package("python-telegram-bot"):
        print("✓ python-telegram-bot installed successfully")
    else:
        print("✗ Failed to install python-telegram-bot")
        print("  You can install manually: pip install python-telegram-bot")
    
    print("\n[2/3] Running Web Scraping...")
    print("-" * 70)
    try:
        from scripts.web_scrapper import AAUWebScraper, get_aau_target_urls
        
        scraper = AAUWebScraper()
        target_urls = get_aau_target_urls()
        
        total_pages = sum(len(urls) for urls in target_urls.values())
        print(f"Scraping {total_pages} pages from AAU website...")
        
        collected_data = scraper.scrape_target_pages(target_urls)
        
        output_path = Path("data/raw/web_collected_data.csv")
        scraper.save_to_csv(collected_data, output_path)
        
        print(f"\n✓ Web scraping complete!")
        print(f"  Collected: {len(collected_data)} Q&A pairs")
        print(f"  Saved to: {output_path}")
        web_count = len(collected_data)
    except Exception as e:
        print(f"\n✗ Web scraping error: {e}")
        import traceback
        traceback.print_exc()
        web_count = 0
    
    print("\n[3/3] Running Telegram Collection...")
    print("-" * 70)
    
    AAU_TELEGRAM_CHANNELS = [
        "https://t.me/aau_official",
        "https://t.me/CTBEAAU",
        "https://t.me/SchoolofCommerceocs",
        "https://t.me/aausc_1943"
    ]
    
    print(f"Channels to collect from:")
    for channel in AAU_TELEGRAM_CHANNELS:
        print(f"  - {channel}")
    
    import os
    api_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    
    if not api_token:
        print("\n⚠ Telegram Bot Token not found in environment.")
        print("  Set TELEGRAM_BOT_TOKEN environment variable or skip Telegram collection.")
        print("  Example: $env:TELEGRAM_BOT_TOKEN='your_token_here'")
    
    telegram_count = 0
    if api_token:
        try:
            from scripts.telegram_cli import TelegramDataCollector, collect_from_telegram_api
            
            channel_usernames = [ch.replace('https://t.me/', '') for ch in AAU_TELEGRAM_CHANNELS]
            
            print(f"\nFetching from {len(channel_usernames)} channels...")
            collector = collect_from_telegram_api(api_token, channel_usernames)
            
            if collector:
                telegram_count = len(collector.collected_data)
                
                if telegram_count > 0:
                    collector.save_to_csv("data/raw/telegram_collected_data.csv", append=False)
                    print(f"\n✓ Telegram collection complete!")
                    print(f"  Collected: {telegram_count} messages")
                    print(f"  Saved to: data/raw/telegram_collected_data.csv")
                else:
                    print(f"\n⚠ No messages collected from Telegram channels")
            else:
                print("\n✗ Failed to initialize Telegram collector")
        except ImportError:
            print("\n✗ python-telegram-bot not installed.")
            print("  Install with: pip install python-telegram-bot")
        except Exception as e:
            print(f"\n✗ Telegram collection error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n⚠ Skipping Telegram collection (no token provided)")
    
    print("\n" + "=" * 70)
    print("Collection Summary")
    print("=" * 70)
    print(f"Web scraping:  {web_count:4d} items -> data/raw/web_collected_data.csv")
    print(f"Telegram:      {telegram_count:4d} items -> data/raw/telegram_collected_data.csv")
    print(f"Total:         {web_count + telegram_count:4d} items")
    
    if web_count + telegram_count > 0:
        print("\nNext steps:")
        print("  1. Process data: python -m app.data_processor")
        print("  2. Generate stats: python scripts/data_stats.py")

if __name__ == "__main__":
    main()
