"""Simple script to run both web scraping and Telegram collection."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("AAU Data Collection - Web Scraping & Telegram")
print("=" * 70)

print("\n[1/2] Starting Web Scraping...")
print("-" * 70)
try:
    from scripts.web_scrapper import AAUWebScraper, get_aau_target_urls
    
    scraper = AAUWebScraper()
    target_urls = get_aau_target_urls()
    
    total_pages = sum(len(urls) for urls in target_urls.values())
    print(f"Will scrape {total_pages} pages from AAU website...")
    
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

print("\n[2/2] Starting Telegram Collection...")
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

api_token = None
if len(sys.argv) > 1:
    api_token = sys.argv[1]
    print(f"\nUsing API token from command line argument")
elif hasattr(sys, 'stdin') and not sys.stdin.isatty():
    api_token = input("\nEnter Telegram Bot API token (or press Enter to skip): ").strip()
else:
    print("\nNo API token provided. Skipping Telegram API collection.")
    print("To collect from Telegram API:")
    print("  1. Get token from @BotFather on Telegram")
    print("  2. Run: python run_collection.py <your_token>")
    print("  3. Or manually export messages and use collect_from_file()")

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
            else:
                telegram_count = 0
        else:
            telegram_count = 0
        
        print(f"\n✓ Telegram collection complete!")
        print(f"  Collected: {telegram_count} messages")
        print(f"  Saved to: data/raw/telegram_collected_data.csv")
    except ImportError:
        print("\n✗ python-telegram-bot not installed.")
        print("  Install with: pip install python-telegram-bot")
    except Exception as e:
        print(f"\n✗ Telegram collection error: {e}")
        import traceback
        traceback.print_exc()

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
else:
    print("\n⚠ No data collected. Check errors above.")
