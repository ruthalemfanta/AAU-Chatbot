"""Web scraper for collecting data from AAU official website."""
import requests
from bs4 import BeautifulSoup
import time
import csv
from pathlib import Path
from datetime import datetime
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AAUWebScraper:
    """Scraper for AAU official website pages."""
    
    def __init__(self, base_url="https://www.aau.edu.et", delay=2):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.robots_parser = RobotFileParser()
        self.robots_parser.set_url(urljoin(base_url, '/robots.txt'))
        try:
            self.robots_parser.read()
        except:
            logger.warning("Could not read robots.txt")
        self.collected_data = []
    
    def can_fetch(self, url):
        """Check if URL can be fetched according to robots.txt."""
        try:
            return self.robots_parser.can_fetch(self.session.headers['User-Agent'], url)
        except:
            return True
    
    def fetch_page(self, url):
        """Fetch a webpage with error handling."""
        if not self.can_fetch(url):
            logger.warning(f"Blocked by robots.txt: {url}")
            return None
        
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=15, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_text_content(self, html_content):
        """Extract all meaningful text content from HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        text_content = []
        
        for element in soup.find_all(['p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'td', 'th']):
            text = element.get_text(strip=True)
            if text and len(text) > 15:
                text_content.append(text)
        
        return text_content
    
    def extract_qa_pairs(self, html_content):
        """Extract Q&A pairs from HTML content with multiple strategies."""
        soup = BeautifulSoup(html_content, 'html.parser')
        qa_pairs = []
        
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        all_text_elements = []
        for element in soup.find_all(['p', 'div', 'li', 'td', 'span']):
            text = element.get_text(strip=True)
            if text and len(text) > 20:
                all_text_elements.append(text)
        
        if len(all_text_elements) > 0:
            logger.debug(f"Found {len(all_text_elements)} text elements on page")
        
        strategy1_pairs = self._extract_faq_patterns(soup)
        strategy2_pairs = self._extract_heading_question_patterns(soup)
        strategy3_pairs = self._extract_list_patterns(soup)
        strategy4_pairs = self._extract_paragraph_questions(soup)
        strategy5_pairs = self._extract_any_questions_from_text(all_text_elements)
        
        all_pairs = strategy1_pairs + strategy2_pairs + strategy3_pairs + strategy4_pairs + strategy5_pairs
        
        seen = set()
        for qa in all_pairs:
            q_key = qa['question'].lower().strip()[:50]
            if q_key not in seen and len(qa['question']) > 10 and len(qa['answer']) > 15:
                seen.add(q_key)
                qa_pairs.append(qa)
        
        return qa_pairs
    
    def _extract_faq_patterns(self, soup):
        """Extract from FAQ-specific HTML patterns."""
        qa_pairs = []
        
        faq_containers = soup.find_all(['dl', 'div', 'section'], 
                                      class_=lambda x: x and any(
                                          keyword in str(x).lower() 
                                          for keyword in ['faq', 'question', 'answer', 'help', 'q&a']
                                      ))
        
        for container in faq_containers:
            questions = container.find_all(['dt', 'h3', 'h4', 'h5', 'strong', 'b', 'span'], 
                                          class_=lambda x: x and 'question' in str(x).lower() if x else False)
            if not questions:
                questions = container.find_all(['dt', 'h3', 'h4', 'h5'])
            
            answers = container.find_all(['dd', 'p', 'div', 'li'])
            
            for q in questions:
                q_text = q.get_text(strip=True)
                if not q_text or len(q_text) < 10:
                    continue
                
                answer_elem = q.find_next(['dd', 'p', 'div', 'li'])
                if not answer_elem:
                    answer_elem = q.find_next_sibling(['dd', 'p', 'div', 'li'])
                
                if answer_elem:
                    a_text = answer_elem.get_text(strip=True)
                    if a_text and len(a_text) > 20 and len(q_text) > 10:
                        qa_pairs.append({
                            'question': q_text,
                            'answer': a_text
                        })
        
        return qa_pairs
    
    def _extract_heading_question_patterns(self, soup):
        """Extract questions from headings followed by answers."""
        qa_pairs = []
        
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for heading in headings:
            text = heading.get_text(strip=True)
            
            is_question = (
                '?' in text or
                any(word in text.lower() for word in ['how', 'what', 'when', 'where', 'why', 'who', 'which', 'can i', 'do i', 'should i']) or
                text.lower().startswith(('how', 'what', 'when', 'where', 'why', 'who', 'which'))
            )
            
            if is_question and len(text) > 10:
                answer_elem = heading.find_next(['p', 'div', 'li', 'td'])
                if not answer_elem:
                    answer_elem = heading.find_next_sibling(['p', 'div', 'li'])
                
                if answer_elem:
                    answer = answer_elem.get_text(strip=True)
                    if answer and len(answer) > 20:
                        qa_pairs.append({
                            'question': text,
                            'answer': answer
                        })
        
        return qa_pairs
    
    def _extract_list_patterns(self, soup):
        """Extract from list patterns (ul/ol with questions)."""
        qa_pairs = []
        
        lists = soup.find_all(['ul', 'ol'])
        
        for list_elem in lists:
            items = list_elem.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                if '?' in text and len(text) > 15:
                    parts = text.split('?', 1)
                    if len(parts) == 2:
                        question = parts[0].strip() + '?'
                        answer = parts[1].strip()
                        if len(question) > 10 and len(answer) > 15:
                            qa_pairs.append({
                                'question': question,
                                'answer': answer
                            })
        
        return qa_pairs
    
    def _extract_paragraph_questions(self, soup):
        """Extract questions from paragraphs."""
        qa_pairs = []
        
        paragraphs = soup.find_all('p')
        
        for para in paragraphs:
            text = para.get_text(strip=True)
            
            if '?' in text and len(text) > 20:
                sentences = re.split(r'[.!?]+', text)
                for i, sentence in enumerate(sentences):
                    if '?' in sentence and len(sentence.strip()) > 10:
                        question = sentence.strip()
                        if not question.endswith('?'):
                            question += '?'
                        
                        answer_parts = sentences[i+1:i+3] if i+1 < len(sentences) else []
                        answer = ' '.join(answer_parts).strip()
                        
                        if answer and len(answer) > 15:
                            qa_pairs.append({
                                'question': question,
                                'answer': answer
                            })
        
        return qa_pairs
    
    def _extract_any_questions_from_text(self, text_elements):
        """Extract any question-like patterns from text elements."""
        qa_pairs = []
        question_patterns = [
            r'(.+\?)\s+(.+)',
            r'(How\s+.+\?)\s+(.+)',
            r'(What\s+.+\?)\s+(.+)',
            r'(When\s+.+\?)\s+(.+)',
            r'(Where\s+.+\?)\s+(.+)',
            r'(Why\s+.+\?)\s+(.+)',
        ]
        
        for text in text_elements:
            for pattern in question_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    question = match.group(1).strip()
                    answer = match.group(2).strip()[:500]
                    if len(question) > 10 and len(answer) > 20:
                        qa_pairs.append({
                            'question': question,
                            'answer': answer
                        })
        
        return qa_pairs
    
    def scrape_page(self, url, page_type="general", debug=False):
        """Scrape a single page and extract Q&A pairs."""
        logger.info(f"Scraping {url} ({page_type})")
        html_content = self.fetch_page(url)
        
        if not html_content:
            logger.warning(f"No content retrieved from {url}")
            return []
        
        if debug:
            debug_file = Path(f"data/raw/debug_{page_type}_{url.split('/')[-1] or 'index'}.html")
            debug_file.parent.mkdir(parents=True, exist_ok=True)
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"Saved HTML debug to {debug_file}")
        
        qa_pairs = self.extract_qa_pairs(html_content)
        logger.info(f"Found {len(qa_pairs)} Q&A pairs from {url}")
        
        if len(qa_pairs) == 0:
            soup = BeautifulSoup(html_content, 'html.parser')
            text_samples = [elem.get_text(strip=True)[:100] for elem in soup.find_all(['p', 'div', 'h1', 'h2', 'h3'])[:5] if elem.get_text(strip=True)]
            if text_samples:
                logger.debug(f"Sample page content: {text_samples}")
        
        return qa_pairs
    
    def scrape_target_pages(self, target_urls):
        """Scrape multiple target pages."""
        all_qa_pairs = []
        
        for page_type, urls in target_urls.items():
            logger.info(f"Scraping {page_type} pages...")
            for url in urls:
                qa_pairs = self.scrape_page(url, page_type)
                for qa in qa_pairs:
                    qa['source'] = 'website'
                    qa['page_type'] = page_type
                    qa['url'] = url
                    qa['date_collected'] = datetime.now().isoformat()
                all_qa_pairs.extend(qa_pairs)
        
        return all_qa_pairs
    
    def save_to_csv(self, data, output_path):
        """Save collected data to CSV file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_exists = output_path.exists()
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'source', 'raw_text', 'cleaned_text', 'date_collected', 
                         'page_type', 'url', 'answer']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for idx, item in enumerate(data, start=1):
                writer.writerow({
                    'id': idx,
                    'source': item.get('source', 'website'),
                    'raw_text': item.get('question', ''),
                    'cleaned_text': '',
                    'date_collected': item.get('date_collected', datetime.now().isoformat()),
                    'page_type': item.get('page_type', 'general'),
                    'url': item.get('url', ''),
                    'answer': item.get('answer', '')
                })
        
        logger.info(f"Saved {len(data)} items to {output_path}")


def get_aau_target_urls():
    """Get target URLs for AAU website."""
    base = "https://www.aau.edu.et"
    
    return {
        'admission': [
            f"{base}/admission",
            f"{base}/admissions",
            f"{base}/admission/requirements",
            f"{base}/admission/process",
            f"{base}/admission/apply",
        ],
        'registration': [
            f"{base}/registration",
            f"{base}/registrar",
            f"{base}/registration/guide",
            f"{base}/student-registration",
        ],
        'fees': [
            f"{base}/fees",
            f"{base}/tuition",
            f"{base}/fees/payment",
            f"{base}/finance",
        ],
        'academic_calendar': [
            f"{base}/academic-calendar",
            f"{base}/calendar",
            f"{base}/academic-schedule",
        ],
        'general': [
            f"{base}/faq",
            f"{base}/help",
            f"{base}/student-services",
            f"{base}/contact",
        ]
    }


if __name__ == "__main__":
    scraper = AAUWebScraper()
    
    target_urls = get_aau_target_urls()
    
    print("AAU Website Scraping")
    print("=" * 60)
    print(f"\nScraping {sum(len(urls) for urls in target_urls.values())} pages...")
    
    collected_data = scraper.scrape_target_pages(target_urls)
    
    output_path = Path("data/raw/web_collected_data.csv")
    scraper.save_to_csv(collected_data, output_path)
    
    print(f"\nCollection complete!")
    print(f"Total Q&A pairs collected: {len(collected_data)}")
    print(f"Data saved to: {output_path}")
