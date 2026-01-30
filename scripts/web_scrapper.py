"""
Web Scraper for AAU Helpdesk Data Collection
Scrapes AAU website and related sources for training data
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AAUWebScraper:
    """Web scraper for AAU website and related sources"""
    
    def __init__(self):
        self.base_urls = [
            "http://www.aau.edu.et",  # Main AAU website
            # Add more AAU-related URLs as needed
        ]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_data = []
        self.delay = 1  # Delay between requests to be respectful
    
    def scrape_aau_pages(self) -> List[Dict[str, Any]]:
        """Scrape AAU website pages for relevant information"""
        scraped_content = []
        
        # Define target pages and their expected intents
        target_pages = {
            '/admission': 'admission_inquiry',
            '/registration': 'registration_help',
            '/fees': 'fee_payment',
            '/academic-services': 'document_request',
            '/student-services': 'general_info',
            '/departments': 'course_information'
        }
        
        for base_url in self.base_urls:
            for page_path, intent in target_pages.items():
                try:
                    url = urljoin(base_url, page_path)
                    content = self._scrape_page(url, intent)
                    if content:
                        scraped_content.extend(content)
                    
                    time.sleep(self.delay)
                    
                except Exception as e:
                    logger.error(f"Error scraping {url}: {e}")
                    continue
        
        return scraped_content
    
    def _scrape_page(self, url: str, intent: str) -> List[Dict[str, Any]]:
        """Scrape a single page and extract relevant content"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            text_content = soup.get_text()
            
            # Clean and process text
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Generate training samples from the content
            samples = self._generate_training_samples(text, intent, url)
            
            logger.info(f"Scraped {len(samples)} samples from {url}")
            return samples
            
        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Parsing error for {url}: {e}")
            return []
    
    def _generate_training_samples(self, text: str, intent: str, source_url: str) -> List[Dict[str, Any]]:
        """Generate training samples from scraped text"""
        samples = []
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Intent-specific keyword patterns
        intent_patterns = {
            'admission_inquiry': [
                r'admission|apply|application|entrance|requirement|eligibility',
                r'how to apply|application process|admission criteria'
            ],
            'registration_help': [
                r'registration|register|enroll|course selection|semester',
                r'how to register|registration process|course enrollment'
            ],
            'fee_payment': [
                r'fee|payment|tuition|cost|price|birr|ETB',
                r'how much|payment method|fee structure'
            ],
            'document_request': [
                r'transcript|certificate|document|diploma|grade report',
                r'request document|official transcript|academic record'
            ],
            'course_information': [
                r'course|curriculum|program|department|faculty|school',
                r'course description|program details|department information'
            ],
            'general_info': [
                r'university|AAU|Addis Ababa University|contact|information',
                r'about university|general information|contact details'
            ]
        }
        
        patterns = intent_patterns.get(intent, [])
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20 or len(sentence) > 200:  # Filter by length
                continue
            
            # Check if sentence matches intent patterns
            if any(re.search(pattern, sentence, re.IGNORECASE) for pattern in patterns):
                # Extract parameters from sentence
                parameters = self._extract_parameters_from_text(sentence)
                
                sample = {
                    'text': sentence,
                    'intent': intent,
                    'parameters': parameters,
                    'source': source_url,
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                samples.append(sample)
        
        return samples[:10]  # Limit samples per page
    
    def _extract_parameters_from_text(self, text: str) -> Dict[str, List[str]]:
        """Extract parameters from text using regex patterns"""
        parameters = {}
        
        # Department patterns
        dept_pattern = r'\b(computer science|engineering|medicine|law|business|economics|psychology|biology|chemistry|physics|mathematics|english|amharic)\b'
        departments = re.findall(dept_pattern, text, re.IGNORECASE)
        if departments:
            parameters['department'] = list(set(departments))
        
        # Document type patterns
        doc_pattern = r'\b(transcript|certificate|diploma|degree|grade report|academic record)\b'
        documents = re.findall(doc_pattern, text, re.IGNORECASE)
        if documents:
            parameters['document_type'] = list(set(documents))
        
        # Year patterns
        year_pattern = r'\b(20\d{2})\b'
        years = re.findall(year_pattern, text)
        if years:
            parameters['year'] = list(set(years))
        
        # Semester patterns
        semester_pattern = r'\b(first|second|third|1st|2nd|3rd|fall|spring|summer)\s*(semester|sem)?\b'
        semesters = re.findall(semester_pattern, text, re.IGNORECASE)
        if semesters:
            parameters['semester'] = list(set([s[0] for s in semesters]))
        
        # Fee amount patterns
        fee_pattern = r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(birr|etb|usd|\$)?\b'
        fees = re.findall(fee_pattern, text, re.IGNORECASE)
        if fees:
            parameters['fee_amount'] = list(set([f[0] for f in fees]))
        
        return parameters
    
    def generate_synthetic_data(self) -> List[Dict[str, Any]]:
        """Generate synthetic training data for AAU helpdesk"""
        synthetic_samples = []
        
        # Templates for generating synthetic queries
        templates = {
            'admission_inquiry': [
                "I want to apply for {department} admission at AAU",
                "What are the requirements for {department} program?",
                "How do I apply to {department} at Addis Ababa University?",
                "When is the application deadline for {department}?",
                "What documents do I need for {department} admission?"
            ],
            'registration_help': [
                "How do I register for {semester} semester {year}?",
                "I need help with course registration for {semester} {year}",
                "What is the registration process for {semester} semester?",
                "When does registration open for {semester} {year}?",
                "I want to register for courses in {semester} semester"
            ],
            'fee_payment': [
                "I need to pay {fee_amount} birr for tuition",
                "How do I pay university fees of {fee_amount}?",
                "What are the payment methods for {fee_amount} ETB?",
                "Where can I pay my {fee_amount} birr semester fee?",
                "I want to pay {fee_amount} for registration"
            ],
            'transcript_request': [
                "I need my {document_type} from {department}",
                "How do I request a {document_type}?",
                "Can I get my {document_type} urgently?",
                "What is the process for {document_type} request?",
                "I want to request my official {document_type}"
            ],
            'grade_inquiry': [
                "What are my grades for {semester} semester {year}?",
                "I want to check my {semester} {year} results",
                "How do I access my grades for {semester} semester?",
                "When will {semester} {year} grades be released?",
                "I need my grade report for {semester} {year}"
            ]
        }
        
        # Parameter values
        departments = ['computer science', 'engineering', 'medicine', 'law', 'business', 'economics']
        semesters = ['first', 'second', 'third', 'fall', 'spring']
        years = ['2023', '2024', '2025']
        documents = ['transcript', 'certificate', 'diploma', 'grade report']
        fees = ['5000', '7500', '10000', '2500', '3000']
        
        # Generate samples
        for intent, template_list in templates.items():
            for template in template_list:
                # Generate multiple variations
                for _ in range(3):
                    params = {}
                    text = template
                    
                    if '{department}' in template:
                        dept = departments[len(synthetic_samples) % len(departments)]
                        text = text.replace('{department}', dept)
                        params['department'] = [dept]
                    
                    if '{semester}' in template:
                        sem = semesters[len(synthetic_samples) % len(semesters)]
                        text = text.replace('{semester}', sem)
                        params['semester'] = [sem]
                    
                    if '{year}' in template:
                        year = years[len(synthetic_samples) % len(years)]
                        text = text.replace('{year}', year)
                        params['year'] = [year]
                    
                    if '{document_type}' in template:
                        doc = documents[len(synthetic_samples) % len(documents)]
                        text = text.replace('{document_type}', doc)
                        params['document_type'] = [doc]
                    
                    if '{fee_amount}' in template:
                        fee = fees[len(synthetic_samples) % len(fees)]
                        text = text.replace('{fee_amount}', fee)
                        params['fee_amount'] = [fee]
                    
                    synthetic_samples.append({
                        'text': text,
                        'intent': intent,
                        'parameters': params,
                        'source': 'synthetic',
                        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        return synthetic_samples
    
    def save_data(self, data: List[Dict[str, Any]], filename: str):
        """Save scraped data to JSON file"""
        output_path = Path('data/raw') / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(data)} samples to {output_path}")
    
    def run_scraping(self):
        """Run the complete scraping process"""
        logger.info("Starting AAU data scraping...")
        
        # Scrape web pages
        web_data = self.scrape_aau_pages()
        
        # Generate synthetic data
        synthetic_data = self.generate_synthetic_data()
        
        # Combine all data
        all_data = web_data + synthetic_data
        
        # Save data
        self.save_data(all_data, 'aau_training_data.json')
        self.save_data(web_data, 'aau_web_scraped.json')
        self.save_data(synthetic_data, 'aau_synthetic_data.json')
        
        logger.info(f"Scraping completed. Total samples: {len(all_data)}")
        return all_data

if __name__ == "__main__":
    scraper = AAUWebScraper()
    data = scraper.run_scraping()
    print(f"Collected {len(data)} training samples")