"""
News Retriever for AAU Helpdesk Chatbot
Searches scraped Telegram data for relevant real-time information
"""

import json
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


def _is_informative(text: str) -> bool:
    """
    Check if text is informative content (not a question or non-useful content)
    Returns True if the content should be included
    """
    text_lower = text.lower().strip()

    # Filter out questions (not informative, user is asking for help)
    question_patterns = [
        text_lower.endswith('?'),
        text_lower.startswith('how do i'),
        text_lower.startswith('how can i'),
        text_lower.startswith('where can i'),
        text_lower.startswith('what is the'),
        text_lower.startswith('when is'),
        text_lower.startswith('can someone'),
        text_lower.startswith('does anyone'),
        text_lower.startswith('is there'),
        text_lower.startswith('please help'),
        text_lower.startswith('i need help'),
        text_lower.startswith('help me'),
        'anyone know' in text_lower,
        'can you help' in text_lower,
        'pls help' in text_lower,
    ]
    if any(question_patterns):
        return False

    # Filter out very short non-informative messages
    if len(text_lower) < 50:
        return False

    # Filter out messages that are mostly hashtags
    words = text_lower.split()
    hashtag_count = sum(1 for w in words if w.startswith('#'))
    if len(words) > 0 and hashtag_count / len(words) > 0.5:
        return False

    # Filter out messages that are mostly emojis or special characters
    alpha_chars = sum(1 for c in text if c.isalpha())
    if len(text) > 0 and alpha_chars / len(text) < 0.3:
        return False

    # Filter out forwarded user questions/requests
    non_informative_phrases = [
        'i want to know',
        'i would like to',
        'can i get',
        'i am looking for',
        'i\'m looking for',
        'how to get',
        'how to apply',
        'need information about',
        'need info about',
        'tell me about',
        'what are the requirements',
        'what documents do i need',
    ]
    if any(phrase in text_lower for phrase in non_informative_phrases):
        # Check if it's actually an announcement answering these questions
        informative_indicators = [
            'we are pleased to announce',
            'announcement',
            'notice',
            'deadline',
            'hereby',
            'informed that',
            'please be informed',
            'application is open',
            'registration is open',
            'results are out',
            'schedule',
            'calendar',
        ]
        if not any(indicator in text_lower for indicator in informative_indicators):
            return False

    return True


class NewsRetriever:
    """Retriever for scraped telegram news and announcements"""
    
    def __init__(self, data_path: str = 'data/raw/telegram_training_data.json'):
        self.data_path = data_path
        self.news_data = self._load_data()
        
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load news data from JSON file"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} news items for retrieval")
            return data
        except FileNotFoundError:
            logger.warning(f"News data file not found: {self.data_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading news data: {e}")
            return []

    def find_relevant_news(self, intent: str, parameters: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Find news items relevant to the intent and parameters
        Returns the most recent matches first
        """
        matches = []
        
        # Intent-related keywords for text matching
        intent_keywords = {
            'admission_inquiry': ['admission', 'apply', 'application', 'enroll', 'entrance', 'exam', 'requirement', 'eligibility', 'accepted', 'acceptance'],
            'registration_help': ['registration', 'register', 'course registration', 'add drop', 'enrollment'],
            'fee_payment': ['fee', 'payment', 'tuition', 'cost', 'scholarship', 'financial', 'bank', 'pay'],
            'transcript_request': ['transcript', 'academic record', 'grade report', 'official document'],
            'grade_inquiry': ['grade', 'result', 'gpa', 'score', 'exam result', 'marks', 'assessment'],
            'course_information': ['course', 'class', 'subject', 'curriculum', 'syllabus', 'program', 'module'],
            'schedule_inquiry': ['schedule', 'timetable', 'calendar', 'academic calendar', 'semester', 'date', 'deadline'],
            'document_request': ['document', 'certificate', 'letter', 'verification', 'official'],
            'technical_support': ['portal', 'system', 'website', 'login', 'password', 'technical', 'error'],
            'general_info': ['university', 'campus', 'aau', 'announcement', 'news', 'event']
        }
        
        # Get keywords for the detected intent
        keywords_for_intent = intent_keywords.get(intent, [])
        
        # Score each news item
        scored_candidates = []
        for item in self.news_data:
            score = 0
            text = item.get('text', '')
            text_lower = text.lower()
            item_intent = item.get('intent', '')
            
            # Skip non-informative content (questions, short posts, hashtag-only, etc.)
            if not _is_informative(text):
                continue
            
            # Boost score for exact intent match
            if item_intent == intent:
                score += 5
            
            # Boost score for intent-related keywords in text
            for keyword in keywords_for_intent:
                if keyword in text_lower:
                    score += 2
            
            # Boost score for parameter matches
            if parameters:
                for key, values in parameters.items():
                    if not values:
                        continue
                    for value in values:
                        if str(value).lower() in text_lower:
                            score += 3  # Strong match for parameter
            
            # Also check item's own parameters for matches
            item_params = item.get('parameters', {})
            if parameters and item_params:
                for key, values in parameters.items():
                    if key in item_params:
                        item_values = item_params.get(key, [])
                        for value in values:
                            if str(value).lower() in [str(v).lower() for v in item_values]:
                                score += 4  # Very strong match
            
            if score > 0:
                scored_candidates.append((score, item))
        
        # Sort: Primary by score (desc), Secondary by date (desc)
        scored_candidates.sort(key=lambda x: (x[0], x[1].get('date', '')), reverse=True)
        
        # Return top N matches
        return [item for score, item in scored_candidates[:limit]]

    def format_news_response(self, news_items: List[Dict[str, Any]]) -> Optional[str]:
        """Format found news items into a readable response"""
        if not news_items:
            return None
            
        intro = "📢 **Related Announcements found from AAU Channels:**\n\n"
        body = ""
        
        for item in news_items:
            date_str = item.get('date', '')[:10] # YYYY-MM-DD
            channel = item.get('channel', 'Unknown Source')
            text = item.get('text', '').strip()
            
            # Truncate very long texts
            if len(text) > 300:
                text = text[:297] + "..."
                
            body += f"🗓 **{date_str}** | {channel}\n{text}\n\n"
            
        return intro + body.strip()
