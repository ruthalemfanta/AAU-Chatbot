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

# Note: This is a simplified version. For full Telegram integration, you would need:
# from telegram import Bot
# from telegram.ext import Application, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramDataCollector:
    """Collect data from Telegram channels for training"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token
        self.collected_messages = []
        
        # AAU-related channel patterns (examples)
        self.aau_channels = [
            '@aau_official',
            '@aau_students',
            '@aau_announcements',
            # Add actual AAU Telegram channels
        ]
        
        # Keywords for filtering relevant messages
        self.relevant_keywords = [
            'admission', 'registration', 'fee', 'payment', 'transcript',
            'certificate', 'grade', 'course', 'semester', 'exam',
            'department', 'faculty', 'student', 'university', 'aau'
        ]
    
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
        fee_pattern = r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(birr|etb|usd|\$)?\b'
        fees = re.findall(fee_pattern, text_lower)
        if fees:
            parameters['fee_amount'] = list(set([f[0] for f in fees]))
        
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
    
    def collect_and_process_data(self):
        """Main method to collect and process Telegram data"""
        logger.info("Starting Telegram data collection...")
        
        # For now, use simulated data
        # In production, you would connect to actual Telegram channels
        raw_messages = self.simulate_telegram_data()
        
        # Filter relevant messages
        relevant_messages = self.filter_relevant_messages(raw_messages)
        
        # Process for training
        training_data = self.process_messages_for_training(relevant_messages)
        
        # Save data
        self.save_training_data(training_data, 'telegram_training_data.json')
        
        logger.info(f"Processed {len(training_data)} messages from Telegram")
        return training_data

class TelegramCLI:
    """Command-line interface for Telegram operations"""
    
    def __init__(self):
        self.collector = TelegramDataCollector()
    
    def run_data_collection(self):
        """Run data collection from Telegram"""
        print("🤖 AAU Helpdesk - Telegram Data Collector")
        print("=" * 50)
        
        try:
            data = self.collector.collect_and_process_data()
            
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
        print("  1. collect - Collect data from Telegram")
        print("  2. sample - Show sample collected data")
        print("  3. quit - Exit")
        print()
        
        while True:
            try:
                command = input("Enter command: ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif command in ['collect', '1']:
                    self.run_data_collection()
                elif command in ['sample', '2']:
                    self.show_sample_data()
                else:
                    print("❌ Unknown command. Try 'collect', 'sample', or 'quit'")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='AAU Helpdesk Telegram CLI')
    parser.add_argument('--collect', action='store_true', help='Collect data from Telegram')
    parser.add_argument('--sample', action='store_true', help='Show sample data')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    cli = TelegramCLI()
    
    if args.collect:
        cli.run_data_collection()
    elif args.sample:
        cli.show_sample_data()
    elif args.interactive:
        cli.run_interactive_mode()
    else:
        # Default to interactive mode
        cli.run_interactive_mode()

if __name__ == "__main__":
    main()