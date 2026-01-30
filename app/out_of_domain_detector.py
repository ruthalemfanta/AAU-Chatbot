"""
Out-of-Domain Detection for AAU Helpdesk Chatbot
Detects queries that are outside the university domain
"""

import re
from typing import Dict, List, Set, Optional
import logging

logger = logging.getLogger(__name__)

class OutOfDomainDetector:
    """Detects queries that are outside AAU university domain"""
    
    def __init__(self):
        # AAU domain keywords
        self.domain_keywords = {
            # University terms
            'aau', 'addis', 'ababa', 'university', 'college', 'school', 'faculty',
            'department', 'academic', 'student', 'campus', 'education',
            
            # Academic processes
            'admission', 'registration', 'enrollment', 'application', 'apply',
            'semester', 'term', 'course', 'class', 'subject', 'curriculum',
            'schedule', 'timetable', 'calendar', 'register', 'courses',
            
            # Documents and records
            'transcript', 'certificate', 'diploma', 'degree', 'grade', 'gpa',
            'record', 'document', 'report', 'result', 'mark', 'score',
            
            # Financial
            'fee', 'tuition', 'payment', 'cost', 'price', 'scholarship',
            'financial', 'aid', 'loan', 'budget',
            
            # Departments
            'engineering', 'medicine', 'law', 'business', 'economics',
            'computer', 'science', 'psychology', 'mathematics', 'physics',
            'chemistry', 'biology', 'english', 'amharic',
            
            # Administrative
            'office', 'contact', 'phone', 'email', 'address', 'location',
            'help', 'support', 'service', 'information', 'inquiry'
        }
        
        # Out-of-domain patterns (regex)
        self.out_of_domain_patterns = [
            # Medical/Health (not university-related)
            r'\b(what is|define|explain|symptoms of|treatment for|cure for)\s+(cancer|diabetes|covid|disease|illness|infection|virus|bacteria)\b',
            r'\b(medical advice|health tips|medicine|drug|medication|doctor|hospital|clinic)\b(?!.*university|aau)',
            
            # Weather
            r'\b(weather|temperature|rain|sunny|cloudy|forecast|climate)\b',
            
            # News/Politics
            r'\b(news|politics|government|president|minister|election|vote|political)\b',
            
            # Entertainment
            r'\b(movie|film|music|song|celebrity|actor|actress|entertainment|tv show|series)\b',
            
            # Sports
            r'\b(football|soccer|basketball|tennis|sports|game|match|player|team)\b(?!.*university|aau)',
            
            # Food/Cooking
            r'\b(recipe|cooking|food|restaurant|meal|dish|ingredient|kitchen)\b',
            
            # Technology (non-academic)
            r'\b(programming|coding|software|app|website|internet|social media)\b(?!.*course|class|university|aau)',
            
            # Travel
            r'\b(travel|vacation|holiday|trip|flight|hotel|tourism|tourist)\b',
            
            # Shopping/Commerce
            r'\b(buy|sell|shop|shopping|price|market|store|product|brand)\b(?!.*university|aau)',
            
            # Restaurant/Food (specific to avoid "Addis" false positive)
            r'\b(restaurant|food|meal|dish|cooking|recipe)\b(?!.*university|aau)',
            
            # Personal questions
            r'\b(how old are you|who are you|what are you|where are you from)\b',
            
            # General knowledge (non-academic)
            r'\b(what is the capital of|who invented|when was.*born|history of)\b(?!.*aau|university)',
            
            # Math problems (not course-related)
            r'^\s*\d+\s*[\+\-\*\/]\s*\d+\s*=?\s*$',
            r'\bsolve\s+\d+[\+\-\*\/]\d+\b',
        ]
        
        # Common out-of-domain topics for classification
        self.topic_patterns = {
            'medical': [
                r'\b(cancer|disease|illness|health|medical|doctor|hospital|medicine|treatment|symptoms)\b'
            ],
            'weather': [
                r'\b(weather|temperature|rain|sunny|cloudy|forecast|climate)\b'
            ],
            'entertainment': [
                r'\b(movie|film|music|song|celebrity|entertainment|tv)\b'
            ],
            'technology': [
                r'\b(programming|coding|software|app|website|internet)\b(?!.*course|university)'
            ],
            'general_knowledge': [
                r'\b(what is|define|explain)\b.*\b(capital|inventor|history)\b(?!.*aau|university)'
            ],
            'personal': [
                r'\b(how old are you|who are you|what are you|where are you from)\b'
            ],
            'math_problem': [
                r'^\s*\d+\s*[\+\-\*\/]\s*\d+\s*=?\s*$'
            ]
        }
    
    def has_domain_keywords(self, text: str) -> bool:
        """Check if text contains AAU domain keywords"""
        words = set(re.findall(r'\b\w+\b', text.lower()))
        return len(words & self.domain_keywords) > 0
    
    def detect_out_of_domain_patterns(self, text: str) -> bool:
        """Check if text matches out-of-domain patterns"""
        text_lower = text.lower()
        
        for pattern in self.out_of_domain_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def classify_topic(self, text: str) -> Optional[str]:
        """Classify the topic of out-of-domain text"""
        text_lower = text.lower()
        
        for topic, patterns in self.topic_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return topic
        
        return 'general'
    
    def detect(self, text: str, intent: str, confidence: float) -> Dict:
        """
        Main detection method
        
        Returns:
            Dict with keys:
            - is_out_of_domain: bool
            - confidence_score: float (0-1, higher = more confident it's out of domain)
            - detected_topic: str
            - reason: str (explanation)
        """
        text_clean = text.strip()
        
        # Quick checks for obvious cases
        if len(text_clean) < 3:
            return {
                'is_out_of_domain': False,
                'confidence_score': 0.0,
                'detected_topic': None,
                'reason': 'text_too_short'
            }
        
        # Check 1: Very low intent confidence + no domain keywords
        has_keywords = self.has_domain_keywords(text)
        matches_patterns = self.detect_out_of_domain_patterns(text)
        
        # Strong indicators of out-of-domain
        if matches_patterns:
            topic = self.classify_topic(text)
            return {
                'is_out_of_domain': True,
                'confidence_score': 0.9,
                'detected_topic': topic,
                'reason': 'matches_out_of_domain_pattern'
            }
        
        # Low confidence + no domain keywords = likely out of domain
        if confidence < 0.15 and not has_keywords:
            topic = self.classify_topic(text)
            return {
                'is_out_of_domain': True,
                'confidence_score': 0.7,
                'detected_topic': topic,
                'reason': 'low_confidence_no_keywords'
            }
        
        # Very low confidence even with some keywords
        if confidence < 0.05:
            topic = self.classify_topic(text)
            return {
                'is_out_of_domain': True,
                'confidence_score': 0.6,
                'detected_topic': topic,
                'reason': 'very_low_confidence'
            }
        
        # Check for questions that are too general
        general_question_patterns = [
            r'^\s*(what|who|when|where|why|how)\s+is\s+\w+\s*\??\s*$',
            r'^\s*(tell me about|explain|define)\s+\w+\s*$'
        ]
        
        for pattern in general_question_patterns:
            if re.search(pattern, text.lower()) and not has_keywords:
                topic = self.classify_topic(text)
                return {
                    'is_out_of_domain': True,
                    'confidence_score': 0.8,
                    'detected_topic': topic,
                    'reason': 'general_question_no_context'
                }
        
        # In domain
        return {
            'is_out_of_domain': False,
            'confidence_score': 0.0,
            'detected_topic': None,
            'reason': 'in_domain'
        }
    
    def get_domain_suggestions(self) -> List[str]:
        """Get list of what the bot can help with"""
        return [
            "• Admission inquiries and requirements",
            "• Course registration assistance", 
            "• Fee payment information",
            "• Transcript and document requests",
            "• Grade inquiries and academic records",
            "• University schedules and contacts",
            "• Department information",
            "• Technical support for student services"
        ]

# Test function
def test_out_of_domain_detector():
    """Test the out-of-domain detector"""
    detector = OutOfDomainDetector()
    
    test_cases = [
        # Out of domain
        ("What is cancer?", True, "medical"),
        ("How's the weather today?", True, "weather"),
        ("Tell me a joke", True, "general"),
        ("What is 2+2?", True, "math_problem"),
        ("Who are you?", True, "personal"),
        ("Best restaurants in Addis", True, "general"),
        
        # In domain
        ("How do I register for courses?", False, None),
        ("I need my transcript", False, None),
        ("AAU admission requirements", False, None),
        ("Computer science department contact", False, None),
        ("Fee payment for semester", False, None),
    ]
    
    print("🧪 Testing Out-of-Domain Detection:")
    print("=" * 50)
    
    for text, expected_ood, expected_topic in test_cases:
        result = detector.detect(text, "general_info", 0.1)
        
        status = "✅" if result['is_out_of_domain'] == expected_ood else "❌"
        print(f"{status} '{text}'")
        print(f"   Expected: OOD={expected_ood}, Got: OOD={result['is_out_of_domain']}")
        print(f"   Topic: {result['detected_topic']}, Confidence: {result['confidence_score']:.2f}")
        print(f"   Reason: {result['reason']}")
        print()

if __name__ == "__main__":
    test_out_of_domain_detector()