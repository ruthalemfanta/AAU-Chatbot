"""Telegram data collection script for AAU-related channels."""
import csv
from pathlib import Path
from datetime import datetime
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramDataCollector:
    """Collector for Telegram channel messages."""
    
    def __init__(self):
        """Initialize the Telegram collector."""
        self.collected_data = []
        self.helpdesk_keywords = [
            'admission', 'register', 'registration', 'fee', 'tuition', 'payment',
            'transcript', 'grade', 'gpa', 'schedule', 'exam', 'class',
            'library', 'dormitory', 'housing', 'graduation', 'department',
            'document', 'certificate', 'semester', 'academic', 'scholarship',
            'financial aid', 'facility', 'campus', 'how', 'what', 'when', 'where',
            'help', 'question', 'inquiry', 'request', 'need', 'want'
        ]
    
    def is_helpdesk_related(self, text):
        """Check if message is helpdesk-related."""
        if not text or len(text) < 10:
            return False
        
        text_lower = text.lower()
        has_question_mark = '?' in text
        has_question_words = any(word in text_lower for word in ['how', 'what', 'when', 'where', 'why', 'who', 'which'])
        has_keywords = any(keyword in text_lower for keyword in self.helpdesk_keywords)
        
        return (has_question_mark or has_question_words) and has_keywords
    
    def anonymize_text(self, text):
        """Remove personal identifiers from text."""
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        text = re.sub(r'\+?251[-.\s]?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{4}', '[PHONE]', text)
        text = re.sub(r'\bUGR/\d+/\d+\b', '[STUDENT_ID]', text)
        text = re.sub(r'\b\d{8,}\b', '[ID_NUMBER]', text)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[URL]', text)
        return text
    
    def process_message(self, message_text, message_id=None, channel_name=None, timestamp=None):
        """Process a single Telegram message."""
        if not message_text:
            return None
        
        anonymized_text = self.anonymize_text(message_text)
        
        if not self.is_helpdesk_related(anonymized_text):
            return None
        
        return {
            'raw_text': anonymized_text,
            'message_id': message_id,
            'channel_name': channel_name,
            'timestamp': timestamp or datetime.now().isoformat(),
            'source': 'telegram'
        }
    
    def collect_from_file(self, file_path):
        """Collect messages from a text file (for manual export)."""
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        logger.info(f"Reading messages from {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                processed = self.process_message(
                    line,
                    message_id=f"file_{line_num}",
                    channel_name=file_path.stem
                )
                
                if processed:
                    self.collected_data.append(processed)
        
        logger.info(f"Collected {len(self.collected_data)} helpdesk-related messages")
    
    def collect_from_list(self, messages):
        """Collect messages from a list."""
        for msg in messages:
            processed = self.process_message(
                msg.get('text', ''),
                message_id=msg.get('id'),
                channel_name=msg.get('channel'),
                timestamp=msg.get('timestamp')
            )
            
            if processed:
                self.collected_data.append(processed)
    
    def save_to_csv(self, output_path, append=False):
        """Save collected data to CSV file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_exists = output_path.exists() and append
        
        with open(output_path, 'a' if append else 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'source', 'raw_text', 'cleaned_text', 'date_collected',
                         'channel_name', 'message_id']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            start_id = 1
            if file_exists:
                with open(output_path, 'r', encoding='utf-8') as read_file:
                    reader = csv.DictReader(read_file)
                    rows = list(reader)
                    if rows:
                        start_id = int(rows[-1]['id']) + 1
            
            for idx, item in enumerate(self.collected_data):
                writer.writerow({
                    'id': start_id + idx,
                    'source': item.get('source', 'telegram'),
                    'raw_text': item.get('raw_text', ''),
                    'cleaned_text': '',
                    'date_collected': item.get('timestamp', datetime.now().isoformat()),
                    'channel_name': item.get('channel_name', ''),
                    'message_id': item.get('message_id', '')
                })
        
        logger.info(f"Saved {len(self.collected_data)} items to {output_path}")


def collect_from_telegram_api(api_token, channel_usernames, collector=None):
    """
    Collect messages from Telegram using python-telegram-bot library.
    
    Args:
        api_token: Telegram Bot API token
        channel_usernames: List of channel usernames (without @ or https://t.me/)
        collector: Optional TelegramDataCollector instance. If None, creates a new one.
    
    Returns:
        TelegramDataCollector instance with collected data
    """
    try:
        from telegram import Bot
        from telegram.error import TelegramError
    except ImportError:
        logger.error("python-telegram-bot not installed. Install with: pip install python-telegram-bot")
        return None
    
    if collector is None:
        collector = TelegramDataCollector()
    
    bot = Bot(token=api_token)
    
    for channel_username in channel_usernames:
        channel_username = channel_username.replace('https://t.me/', '').replace('@', '')
        logger.info(f"Fetching messages from {channel_username}...")
        
        try:
            chat = bot.get_chat(f"@{channel_username}")
            messages = []
            
            for message in bot.get_chat_history(chat.id, limit=1000):
                if message.text:
                    processed = collector.process_message(
                        message.text,
                        message_id=str(message.message_id),
                        channel_name=channel_username,
                        timestamp=message.date.isoformat() if message.date else None
                    )
                    if processed:
                        messages.append(processed)
            
            collector.collected_data.extend(messages)
            logger.info(f"Collected {len(messages)} messages from {channel_username}")
            
        except TelegramError as e:
            logger.error(f"Error fetching from {channel_username}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error with {channel_username}: {e}")
    
    return collector


if __name__ == "__main__":
    AAU_TELEGRAM_CHANNELS = [
        "https://t.me/aau_official",
        "https://t.me/CTBEAAU",
        "https://t.me/SchoolofCommerceocs",
        "https://t.me/aausc_1943"
    ]
    
    collector = TelegramDataCollector()
    
    print("Telegram Data Collection")
    print("=" * 60)
    print("\nChannels to collect from:")
    for channel in AAU_TELEGRAM_CHANNELS:
        print(f"  - {channel}")
    
    print("\nNote: To collect from Telegram API, you need:")
    print("1. Telegram Bot API token (get from @BotFather)")
    print("2. python-telegram-bot library: pip install python-telegram-bot")
    print("3. Bot must be added to channels as admin (for private channels)")
    print("\nFor now, you can manually export messages and use collect_from_file()")
    
    api_token = input("\nEnter Telegram Bot API token (or press Enter to skip): ").strip()
    
    if api_token:
        channel_usernames = [ch.replace('https://t.me/', '') for ch in AAU_TELEGRAM_CHANNELS]
        collector = collect_from_telegram_api(api_token, channel_usernames, collector)
        if collector:
            collector.save_to_csv("data/raw/telegram_collected_data.csv", append=False)
            print(f"\nCollection complete! Total messages: {len(collector.collected_data)}")
            print(f"Data saved to: data/raw/telegram_collected_data.csv")
    else:
        print("\nSkipping API collection. Use manual export method instead.")
        print("Export messages from Telegram channels and save to data/raw/telegram_export.txt")
