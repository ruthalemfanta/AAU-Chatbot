"""
Telegram CLI for AAU Helpdesk Chatbot
Provides command-line interface to interact with Telegram channels and collect data
"""

import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re
from pathlib import Path
import argparse
import os

# Telethon for scraping Telegram channels
try:
    from telethon import TelegramClient
    from telethon.tl.types import Message, Channel, Chat
    from telethon.errors import FloodWaitError, ChannelPrivateError
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    print("⚠️ Telethon not installed. Run: pip install telethon")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramDataCollector:
    """Collect data from Telegram channels for training"""
    
    def __init__(self, api_id: Optional[str] = None, api_hash: Optional[str] = None):
        # Get credentials from environment variables or parameters
        self.api_id = api_id or os.getenv('TELEGRAM_API_ID')
        self.api_hash = api_hash or os.getenv('TELEGRAM_API_HASH')
        self.client = None
        self.collected_messages = []
        
        # AAU-related channel patterns (add your actual channels)
        self.aau_channels = [
            '@aau_official',
            '@aau2025_UGStudents',
            '@ctbe_student_council',
            '@Hsquareedu',
            '@CNCS_studentCouncil',
            '@PECCAAiT',
            '@AAiTSiTEnoticeboard',
            '@febinformation',
            '@collegeofss',
            '@aau_stu_union',
            '@CTBEAAU',
            '@SchoolofCommerceocs'
        ]
        
        # Keywords for filtering relevant messages
        self.relevant_keywords = [
            'admission', 'registration', 'fee', 'payment', 'transcript',
            'certificate', 'grade', 'course', 'semester', 'exam',
            'department', 'faculty', 'student', 'university', 'aau'
        ]
    
    async def connect(self) -> bool:
        """Connect to Telegram using Telethon"""
        if not TELETHON_AVAILABLE:
            logger.error("Telethon is not installed. Run: pip install telethon")
            return False
        
        if not self.api_id or not self.api_hash:
            logger.error("Telegram API credentials not set. Set TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables.")
            return False
        
        try:
            # Create session file in scripts directory
            session_path = Path(__file__).parent / 'telegram_session'
            self.client = TelegramClient(str(session_path), int(self.api_id), self.api_hash)
            await self.client.start()
            logger.info("✅ Connected to Telegram successfully!")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Telegram: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Telegram"""
        if self.client:
            await self.client.disconnect()
            logger.info("Disconnected from Telegram")
    
    async def scrape_channel(self, channel: str, limit: int = 50000,
                             days_back: int = 3650) -> List[Dict[str, Any]]:
        """
        Scrape messages from a Telegram channel
        
        Args:
            channel: Channel username (e.g., '@channel_name') or channel ID
            limit: Maximum number of messages to fetch
            days_back: Only fetch messages from the last N days
        
        Returns:
            List of message dictionaries
        """
        messages = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        try:
            logger.info(f"📥 Scraping channel: {channel}")
            
            async for message in self.client.iter_messages(channel, limit=limit):
                # Skip if message is too old
                if message.date.replace(tzinfo=None) < cutoff_date:
                    break
                
                # Skip non-text messages
                if not message.text:
                    continue
                
                msg_data = {
                    "message_id": message.id,
                    "text": message.text,
                    "channel": channel,
                    "date": message.date.isoformat(),
                    "views": getattr(message, 'views', 0),
                    "forwards": getattr(message, 'forwards', 0),
                    "reply_to": message.reply_to_msg_id if message.reply_to else None
                }
                messages.append(msg_data)
            
            logger.info(f"✅ Scraped {len(messages)} messages from {channel}")
            
        except ChannelPrivateError:
            logger.warning(f"⚠️ Cannot access private channel: {channel}")
        except FloodWaitError as e:
            logger.warning(f"⚠️ Rate limited. Need to wait {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            logger.error(f"❌ Error scraping {channel}: {e}")
        
        return messages
    
    async def scrape_all_channels(self, limit: int = 500, 
                                   days_back: int = 365) -> List[Dict[str, Any]]:
        """Scrape messages from all configured AAU channels"""
        all_messages = []
        
        for channel in self.aau_channels:
            try:
                messages = await self.scrape_channel(channel, limit, days_back)
                all_messages.extend(messages)
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error with channel {channel}: {e}")
                continue
        
        return all_messages
    
    async def search_telegram(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for messages across Telegram (global search)
        
        Args:
            query: Search query (e.g., "AAU admission")
            limit: Maximum results
        
        Returns:
            List of matching messages
        """
        messages = []
        
        try:
            logger.info(f"🔍 Searching Telegram for: {query}")
            
            async for message in self.client.iter_messages(None, search=query, limit=limit):
                if not message.text:
                    continue
                
                # Get channel/chat name
                chat_name = "unknown"
                if hasattr(message.chat, 'username') and message.chat.username:
                    chat_name = f"@{message.chat.username}"
                elif hasattr(message.chat, 'title'):
                    chat_name = message.chat.title
                
                msg_data = {
                    "message_id": message.id,
                    "text": message.text,
                    "channel": chat_name,
                    "date": message.date.isoformat(),
                }
                messages.append(msg_data)
            
            logger.info(f"✅ Found {len(messages)} messages for query: {query}")
            
        except Exception as e:
            logger.error(f"❌ Search error: {e}")
        
        return messages
    
    def simulate_telegram_data(self) -> List[Dict[str, Any]]:
        """Simulate Telegram channel data for development/testing"""
        simulated_messages = [
            {
                "message_id": 1,
                "text": "How do I apply for computer science admission at AAU?",
                "channel": "@aau_students",
                "date": "2024-01-15T10:30:00",
                "intent": "admission_inquiry",
                "parameters": {"department": ["computer science"]}
            },
            {
                "message_id": 2,
                "text": "When is the registration deadline for second semester 2024?",
                "channel": "@aau_official",
                "date": "2024-01-16T14:20:00",
                "intent": "registration_help",
                "parameters": {"semester": ["second"], "year": ["2024"]}
            },
            {
                "message_id": 3,
                "text": "I need to pay 7500 birr for my tuition fees. Where can I pay?",
                "channel": "@aau_students",
                "date": "2024-01-17T09:15:00",
                "intent": "fee_payment",
                "parameters": {"fee_amount": ["7500"]}
            },
            {
                "message_id": 4,
                "text": "How can I get my transcript from the engineering department?",
                "channel": "@aau_students",
                "date": "2024-01-18T16:45:00",
                "intent": "transcript_request",
                "parameters": {"document_type": ["transcript"], "department": ["engineering"]}
            },
            {
                "message_id": 5,
                "text": "What are the requirements for medicine program admission?",
                "channel": "@aau_official",
                "date": "2024-01-19T11:30:00",
                "intent": "admission_inquiry",
                "parameters": {"department": ["medicine"]}
            },
            {
                "message_id": 6,
                "text": "I can't access my student portal. Need technical help.",
                "channel": "@aau_students",
                "date": "2024-01-20T13:20:00",
                "intent": "technical_support",
                "parameters": {}
            },
            {
                "message_id": 7,
                "text": "When will first semester 2024 grades be released?",
                "channel": "@aau_announcements",
                "date": "2024-01-21T08:00:00",
                "intent": "grade_inquiry",
                "parameters": {"semester": ["first"], "year": ["2024"]}
            },
            {
                "message_id": 8,
                "text": "What courses are available in the business department?",
                "channel": "@aau_students",
                "date": "2024-01-22T15:10:00",
                "intent": "course_information",
                "parameters": {"department": ["business"]}
            },
            {
                "message_id": 9,
                "text": "I need my degree certificate urgently. How long does it take?",
                "channel": "@aau_students",
                "date": "2024-01-23T12:40:00",
                "intent": "document_request",
                "parameters": {"document_type": ["degree certificate"]}
            },
            {
                "message_id": 10,
                "text": "What is the class schedule for third semester 2024?",
                "channel": "@aau_official",
                "date": "2024-01-24T10:15:00",
                "intent": "schedule_inquiry",
                "parameters": {"semester": ["third"], "year": ["2024"]}
            }
        ]
        
        return simulated_messages
    
    def filter_relevant_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter messages that are relevant to AAU helpdesk"""
        relevant_messages = []
        
        for message in messages:
            text = message.get('text', '').lower()
            
            # Check if message contains relevant keywords
            if any(keyword in text for keyword in self.relevant_keywords):
                relevant_messages.append(message)
        
        return relevant_messages
    
    def extract_intent_from_message(self, text: str) -> str:
        """Extract likely intent from message text"""
        text_lower = text.lower()
        
        # Intent patterns
        intent_patterns = {
            'admission_inquiry': [
                r'admission|apply|application|entrance|requirement',
                r'how to apply|want to apply|applying for'
            ],
            'registration_help': [
                r'registration|register|enroll|course selection',
                r'how to register|registration process|register for'
            ],
            'fee_payment': [
                r'fee|payment|pay|tuition|cost|birr|etb',
                r'how much|payment method|where to pay|need to pay'
            ],
            'transcript_request': [
                r'transcript|certificate|document|diploma',
                r'need transcript|get transcript|request transcript'
            ],
            'grade_inquiry': [
                r'grade|result|score|mark|gpa',
                r'my grades|check grades|grade report|results'
            ],
            'course_information': [
                r'course|curriculum|program|subject',
                r'what courses|course information|available courses'
            ],
            'schedule_inquiry': [
                r'schedule|timetable|class time|when',
                r'class schedule|time table|schedule for'
            ],
            'document_request': [
                r'document|certificate|letter|verification',
                r'need document|request document|official document'
            ],
            'technical_support': [
                r'portal|website|login|access|technical|system',
                r'can\'t access|login problem|technical issue'
            ]
        }
        
        # Check patterns and return most likely intent
        for intent, patterns in intent_patterns.items():
            if any(re.search(pattern, text_lower) for pattern in patterns):
                return intent
        
        return 'general_info'
    
    def extract_parameters_from_message(self, text: str) -> Dict[str, List[str]]:
        """Extract parameters from message text"""
        parameters = {}
        text_lower = text.lower()
        
        # Department extraction
        dept_pattern = r'\b(computer science|cs|engineering|medicine|law|business|economics|psychology|biology|chemistry|physics|mathematics|english|amharic)\b'
        departments = re.findall(dept_pattern, text_lower)
        if departments:
            parameters['department'] = list(set(departments))
        
        # Document type extraction
        doc_pattern = r'\b(transcript|certificate|diploma|degree|grade report|academic record|student id)\b'
        documents = re.findall(doc_pattern, text_lower)
        if documents:
            parameters['document_type'] = list(set(documents))
        
        # Semester extraction
        sem_pattern = r'\b(first|second|third|1st|2nd|3rd|fall|spring|summer)\s*(semester|sem)?\b'
        semesters = re.findall(sem_pattern, text_lower)
        if semesters:
            parameters['semester'] = list(set([s[0] for s in semesters]))
        
        # Year extraction
        year_pattern = r'\b(20\d{2})\b'
        years = re.findall(year_pattern, text)
        if years:
            parameters['year'] = list(set(years))
        
        # Fee amount extraction
        # Improved regex to ignore small numbers (dates, pages) and require currency context if small
        # Looks for numbers > 100 or numbers associated with currency keywords
        fee_pattern = r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(birr|etb|usd|\$)\b'
        fees_with_currency = re.findall(fee_pattern, text_lower)
        
        # Also look for large numbers (likely fees) without currency, but avoid years (20XX)
        raw_numbers = re.findall(r'\b(\d{3,})\b', text)
        large_fees = []
        for num in raw_numbers:
             n = int(num.replace(',', ''))
             if 100 <= n <= 50000 and not (2010 <= n <= 2030): # Avoid years
                 large_fees.append(num)

        valid_fees = []
        if fees_with_currency:
             valid_fees.extend([f[0] for f in fees_with_currency])
        if large_fees:
             valid_fees.extend(large_fees)
             
        if valid_fees:
            parameters['fee_amount'] = list(set(valid_fees))
        
        return parameters
    
    def process_messages_for_training(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process messages to create training data"""
        training_data = []
        
        for message in messages:
            text = message.get('text', '')
            if not text or len(text.strip()) < 10:
                continue
            
            # Extract intent and parameters
            intent = message.get('intent') or self.extract_intent_from_message(text)
            parameters = message.get('parameters') or self.extract_parameters_from_message(text)
            
            training_sample = {
                'text': text.strip(),
                'intent': intent,
                'parameters': parameters,
                'source': 'telegram',
                'channel': message.get('channel', 'unknown'),
                'message_id': message.get('message_id'),
                'date': message.get('date'),
                'processed_at': datetime.now().isoformat()
            }
            
            training_data.append(training_sample)
        
        return training_data
    
    def save_training_data(self, data: List[Dict[str, Any]], filename: str):
        """Save training data to file"""
        output_path = Path('data/raw') / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(data)} training samples to {output_path}")
    
    def collect_and_process_data(self, use_real_api: bool = True, 
                                 limit: int = 100, days_back: int = 30):
        """
        Main method to collect and process Telegram data
        
        Args:
            use_real_api: If True, connect to real Telegram. If False, use simulated data.
            limit: Max messages per channel
            days_back: Only fetch messages from last N days
        """
        logger.info("Starting Telegram data collection...")
        
        if use_real_api and TELETHON_AVAILABLE:
            # Use real Telegram API
            raw_messages = asyncio.get_event_loop().run_until_complete(
                self._collect_real_data(limit, days_back)
            )
        else:
            # Fallback to simulated data
            logger.info("Using simulated data (set use_real_api=True for real scraping)")
            raw_messages = self.simulate_telegram_data()
        
        # Filter relevant messages
        relevant_messages = self.filter_relevant_messages(raw_messages)
        
        # Process for training
        training_data = self.process_messages_for_training(relevant_messages)
        
        # Save data
        self.save_training_data(training_data, 'telegram_training_data.json')
        
        logger.info(f"Processed {len(training_data)} messages from Telegram")
        return training_data
    
    async def _collect_real_data(self, limit: int, days_back: int) -> List[Dict[str, Any]]:
        """Internal method to collect real Telegram data"""
        connected = await self.connect()
        if not connected:
            logger.warning("Could not connect to Telegram, falling back to simulated data")
            return self.simulate_telegram_data()
        
        try:
            messages = await self.scrape_all_channels(limit, days_back)
            return messages
        finally:
            await self.disconnect()

class TelegramCLI:
    """Command-line interface for Telegram operations"""
    
    def __init__(self):
        self.collector = TelegramDataCollector()
    
    def run_data_collection(self, use_real_api: bool = True, limit: int = 100, days_back: int = 30):
        """Run data collection from Telegram"""
        print("🤖 AAU Helpdesk - Telegram Data Collector")
        print("=" * 50)
        
        if use_real_api and not TELETHON_AVAILABLE:
            print("⚠️ Telethon not installed. Install with: pip install telethon")
            print("   Falling back to simulated data...")
            use_real_api = False
        
        if use_real_api and not (self.collector.api_id and self.collector.api_hash):
            print("⚠️ Telegram API credentials not set.")
            print("   Set environment variables:")
            print("   export TELEGRAM_API_ID='your_api_id'")
            print("   export TELEGRAM_API_HASH='your_api_hash'")
            print("   Get credentials at: https://my.telegram.org/apps")
            print("\n   Falling back to simulated data...")
            use_real_api = False
        
        try:
            data = self.collector.collect_and_process_data(
                use_real_api=use_real_api,
                limit=limit,
                days_back=days_back
            )
            
            print(f"\n✅ Successfully collected {len(data)} training samples")
            print("\n📊 Intent Distribution:")
            
            # Show intent distribution
            intent_counts = {}
            for item in data:
                intent = item['intent']
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            for intent, count in sorted(intent_counts.items()):
                print(f"  {intent}: {count} samples")
            
            print(f"\n💾 Data saved to: data/raw/telegram_training_data.json")
            
        except Exception as e:
            print(f"❌ Error during data collection: {e}")
            logger.error(f"Data collection failed: {e}")
    
    def run_channel_scrape(self, channel: str, limit: int = 100, days_back: int = 30):
        """Scrape a specific channel"""
        print(f"🤖 Scraping channel: {channel}")
        print("=" * 50)
        
        if not TELETHON_AVAILABLE:
            print("❌ Telethon not installed. Run: pip install telethon")
            return
        
        async def scrape():
            connected = await self.collector.connect()
            if not connected:
                print("❌ Could not connect to Telegram")
                return []
            
            try:
                messages = await self.collector.scrape_channel(channel, limit, days_back)
                return messages
            finally:
                await self.collector.disconnect()
        
        messages = asyncio.get_event_loop().run_until_complete(scrape())
        
        if messages:
            # Process and save
            training_data = self.collector.process_messages_for_training(messages)
            filename = f"telegram_{channel.replace('@', '')}_data.json"
            self.collector.save_training_data(training_data, filename)
            print(f"\n✅ Scraped {len(messages)} messages")
            print(f"💾 Saved to: data/raw/{filename}")
        else:
            print("❌ No messages collected")
    
    def run_search(self, query: str, limit: int = 50):
        """Search Telegram for messages"""
        print(f"🔍 Searching Telegram for: {query}")
        print("=" * 50)
        
        if not TELETHON_AVAILABLE:
            print("❌ Telethon not installed. Run: pip install telethon")
            return
        
        async def search():
            connected = await self.collector.connect()
            if not connected:
                print("❌ Could not connect to Telegram")
                return []
            
            try:
                messages = await self.collector.search_telegram(query, limit)
                return messages
            finally:
                await self.collector.disconnect()
        
        messages = asyncio.get_event_loop().run_until_complete(search())
        
        if messages:
            training_data = self.collector.process_messages_for_training(messages)
            safe_query = re.sub(r'[^\w\s]', '', query).replace(' ', '_')[:20]
            filename = f"telegram_search_{safe_query}.json"
            self.collector.save_training_data(training_data, filename)
            print(f"\n✅ Found {len(messages)} messages")
            print(f"💾 Saved to: data/raw/{filename}")
        else:
            print("❌ No messages found")
    
    def show_sample_data(self):
        """Show sample collected data"""
        try:
            data_path = Path('data/raw/telegram_training_data.json')
            if not data_path.exists():
                print("❌ No training data found. Run data collection first.")
                return
            
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print("📋 Sample Training Data:")
            print("=" * 50)
            
            for i, sample in enumerate(data[:5]):  # Show first 5 samples
                print(f"\n{i+1}. Text: {sample['text']}")
                print(f"   Intent: {sample['intent']}")
                print(f"   Parameters: {sample['parameters']}")
                print(f"   Source: {sample['source']}")
        
        except Exception as e:
            print(f"❌ Error reading data: {e}")
    
    def run_interactive_mode(self):
        """Run interactive CLI mode"""
        print("🤖 AAU Helpdesk - Telegram CLI")
        print("=" * 40)
        print("Commands:")
        print("  1. collect     - Collect data from all configured channels")
        print("  2. scrape      - Scrape a specific channel")
        print("  3. search      - Search Telegram for messages")
        print("  4. sample      - Show sample collected data")
        print("  5. simulate    - Collect simulated data (no API needed)")
        print("  6. quit        - Exit")
        print()
        
        while True:
            try:
                command = input("Enter command: ").strip().lower()
                
                if command in ['quit', 'exit', 'q', '6']:
                    print("👋 Goodbye!")
                    break
                elif command in ['collect', '1']:
                    self.run_data_collection(use_real_api=True)
                elif command in ['scrape', '2']:
                    channel = input("Enter channel username (e.g., @channel_name): ").strip()
                    if channel:
                        self.run_channel_scrape(channel)
                    else:
                        print("❌ No channel provided")
                elif command in ['search', '3']:
                    query = input("Enter search query: ").strip()
                    if query:
                        self.run_search(query)
                    else:
                        print("❌ No query provided")
                elif command in ['sample', '4']:
                    self.show_sample_data()
                elif command in ['simulate', '5']:
                    self.run_data_collection(use_real_api=False)
                else:
                    print("❌ Unknown command. Try 'collect', 'scrape', 'search', 'sample', 'simulate', or 'quit'")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='AAU Helpdesk Telegram CLI')
    parser.add_argument('--collect', action='store_true', help='Collect data from all configured Telegram channels')
    parser.add_argument('--simulate', action='store_true', help='Use simulated data (no API needed)')
    parser.add_argument('--scrape', type=str, metavar='CHANNEL', help='Scrape a specific channel (e.g., @channel_name)')
    parser.add_argument('--search', type=str, metavar='QUERY', help='Search Telegram for messages')
    parser.add_argument('--sample', action='store_true', help='Show sample data')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--limit', type=int, default=500, help='Max messages to fetch per channel (default: 500)')
    parser.add_argument('--days', type=int, default=365, help='Fetch messages from last N days (default: 365)')
    parser.add_argument('--api-id', type=str, help='Telegram API ID (or set TELEGRAM_API_ID env var)')
    parser.add_argument('--api-hash', type=str, help='Telegram API Hash (or set TELEGRAM_API_HASH env var)')
    
    args = parser.parse_args()
    
    # Set API credentials if provided via command line
    if args.api_id:
        os.environ['TELEGRAM_API_ID'] = args.api_id
    if args.api_hash:
        os.environ['TELEGRAM_API_HASH'] = args.api_hash
    
    cli = TelegramCLI()
    
    if args.collect:
        cli.run_data_collection(use_real_api=True, limit=args.limit, days_back=args.days)
    elif args.simulate:
        cli.run_data_collection(use_real_api=False)
    elif args.scrape:
        cli.run_channel_scrape(args.scrape, limit=args.limit, days_back=args.days)
    elif args.search:
        cli.run_search(args.search, limit=args.limit)
    elif args.sample:
        cli.show_sample_data()
    elif args.interactive:
        cli.run_interactive_mode()
    else:
        # Default to interactive mode
        cli.run_interactive_mode()

if __name__ == "__main__":
    main()