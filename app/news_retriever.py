"""
News Retriever for AAU Helpdesk Chatbot
Searches scraped Telegram data for relevant real-time information
"""

import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

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
            
    def find_relevant_news(self, intent: str, parameters: Dict[str, Any], limit: int = 1) -> List[Dict[str, Any]]:
        """
        Find news items relevant to the intent and parameters
        Returns the most recent matches first
        """
        matches = []
        
        # Filter by intent first (if the news item categorizes it)
        # Note: Our telegram scraper assigns intents, so we can use that!
        candidates = [item for item in self.news_data if item.get('intent') == intent]
        
        # If no candidates match intent directly, look at all 'general_info' too
        if not candidates:
            candidates = [item for item in self.news_data if item.get('intent') == 'general_info']
            
        # Score each candidate
        scored_candidates = []
        for item in candidates:
            score = 0
            text = item.get('text', '').lower()
            
            # Boost score for parameter matches
            # e.g. if user asks about "engineering", boost posts containing "engineering"
            if parameters:
                for key, values in parameters.items():
                    if not values:
                        continue
                    for value in values:
                        if str(value).lower() in text:
                            score += 2 # Strong match
            
            # Boost score for recency
            try:
                date_str = item.get('date')
                if date_str:
                    # Parse ISO format roughly
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    # More recent = higher score (simple implication)
                    # We'll just sort by date at the end, but score helps filter relevance
            except:
                pass
                
            if score > 0 or (not parameters and len(text) > 20):
                 # If we have matches, or if it's a general query, keep it
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
