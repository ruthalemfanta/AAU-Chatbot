# Data Collection Guide - Milestone 2

## Overview

This guide explains how to use the data collection scripts for Milestone 2.

## Components

### 1. Web Scraper (`scripts/web_scrapper.py`)

Scrapes AAU official website pages to collect Q&A pairs.

**Usage:**
```bash
python scripts/web_scrapper.py
```

**Features:**
- Respects robots.txt
- Rate limiting (2 second delay between requests)
- Extracts Q&A pairs from FAQ sections
- Supports multiple page types (admission, registration, fees, etc.)

**Configuration:**
- Update `get_default_target_urls()` function with actual AAU website URLs
- Adjust `delay` parameter for rate limiting
- Modify `base_url` if AAU website URL is different

**Output:**
- Saves to `data/raw/collected_data.csv`

### 2. Telegram Collector (`scripts/telegram_cli.py`)

Collects helpdesk-related questions from Telegram channels.

**Usage:**
```bash
python scripts/telegram_cli.py
```

**Features:**
- Filters helpdesk-related messages
- Anonymizes personal information (emails, phone numbers, IDs)
- Supports manual file import
- Can integrate with Telegram API (requires setup)

**Methods:**
1. **From text file:** Export Telegram messages to a text file, then use `collect_from_file()`
2. **From list:** Provide a list of message dictionaries
3. **From API:** Use `collect_from_telegram_api()` (requires python-telegram-bot library)

**Output:**
- Appends to `data/raw/collected_data.csv`

### 3. Data Processor (`app/data_processor.py`)

Cleans and normalizes collected data.

**Usage:**
```bash
python -m app.data_processor
```

**Features:**
- Text normalization (lowercase, remove extra spaces)
- Special character removal (keeps essential punctuation)
- Language detection (English/Amharic)
- Duplicate removal
- CSV processing

**Output:**
- Saves to `data/processed/cleaned_data.csv`

### 4. Data Statistics (`scripts/data_stats.py`)

Generates statistics report for collected data.

**Usage:**
```bash
python scripts/data_stats.py
```

**Features:**
- Source distribution (website vs telegram)
- Text length statistics
- Language distribution
- Page type distribution
- Channel distribution

**Output:**
- Saves to `reports/data_statistics.txt`
- Prints to console

## Data Format

### Raw Data CSV (`data/raw/collected_data.csv`)

```csv
id,source,raw_text,cleaned_text,date_collected,page_type,url,answer,channel_name,message_id
1,website,"What are admission requirements?","",2024-01-15T10:00:00,admission,https://...,"You need...",,
2,telegram,"How do I register?","",2024-01-15T10:05:00,,,,"aau_students",msg_123
```

### Cleaned Data CSV (`data/processed/cleaned_data.csv`)

Same format as raw data, but with:
- `cleaned_text` field populated
- `language` field added (en/am/mixed/unknown)
- Duplicates removed

## Workflow

1. **Collect from Website:**
   ```bash
   python scripts/web_scrapper.py
   ```

2. **Collect from Telegram:**
   ```bash
   python scripts/telegram_cli.py
   ```

3. **Process Data:**
   ```bash
   python -m app.data_processor
   ```

4. **Generate Statistics:**
   ```bash
   python scripts/data_stats.py
   ```

## Notes

- **Privacy:** All personal identifiers are removed/anonymized
- **Rate Limiting:** Web scraper includes delays to respect server resources
- **Robots.txt:** Web scraper checks robots.txt before scraping
- **Minimum Data:** Target is 500+ questions for training
- **Sources:** Data should come from both website and Telegram

## Troubleshooting

- **No data collected:** Check URLs in web_scrapper.py are correct
- **Telegram API errors:** Ensure python-telegram-bot is installed and configured
- **Processing errors:** Check CSV file format and encoding (should be UTF-8)
- **Empty statistics:** Ensure data files exist and contain data
