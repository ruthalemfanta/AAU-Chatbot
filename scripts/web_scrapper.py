import json
import time
import logging
from typing import List, Dict, Any, Set
from pathlib import Path
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag
import re
from datetime import datetime
import schedule

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from bs4 import BeautifulSoup
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("ERROR: Selenium not installed. Install with: pip install selenium webdriver-manager")
    exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aau_chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AAUWebScraper:
    
    def __init__(self):
        self.base_url = "https://www.aau.edu.et"
        self.domain = urlparse(self.base_url).netloc
        self.visited_urls: Set[str] = set()
        self.to_visit: deque = deque()
        self.scraped_by_category: Dict[str, List[Dict[str, Any]]] = {
            'admission': [],
            'registration': [],
            'fees': [],
            'documents': [],
            'grades': [],
            'courses': [],
            'events': [],
            'news': [],
            'research': [],
            'library': [],
            'general': []
        }
        self.delay = 3
        self.max_pages = 1000
        self.driver = None
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("WebDriver initialized")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()
    
    def normalize_url(self, url: str) -> str:
        url, _ = urldefrag(url)
        url = url.rstrip('/')
        return url
    
    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        
        if parsed.netloc and parsed.netloc != self.domain:
            return False
        
        skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.doc', '.docx', 
                          '.xls', '.xlsx', '.ppt', '.pptx', '.mp4', '.mp3', '.avi']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False
        
        skip_patterns = ['mailto:', 'tel:', 'javascript:', 'wp-content/uploads', 'wp-admin']
        if any(pattern in url.lower() for pattern in skip_patterns):
            return False
        
        return True
    
    def crawl_page(self, url: str) -> Dict[str, Any]:
        try:
            logger.info(f"Loading: {url}")
            self.driver.get(url)
            time.sleep(self.delay)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                logger.warning(f"Timeout: {url}")
            
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            page_data = self._extract_page_content(soup, url)
            links = self._extract_links(soup, url)
            
            return {'page_data': page_data, 'links': links}
            
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            return {'page_data': None, 'links': []}
    
    def _extract_page_content(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe']):
            element.decompose()
        
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ''
        
        headings = []
        for heading_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(heading_tag):
                heading_text = heading.get_text().strip()
                if heading_text and len(heading_text) > 3:
                    headings.append({'level': heading_tag, 'text': heading_text})
        
        paragraphs = []
        for p in soup.find_all('p'):
            p_text = p.get_text().strip()
            if p_text and len(p_text) > 20:
                paragraphs.append(p_text)
        
        lists = []
        for ul in soup.find_all(['ul', 'ol']):
            list_items = [li.get_text().strip() for li in ul.find_all('li') if li.get_text().strip()]
            if list_items:
                lists.extend(list_items)
        
        divs = []
        for div in soup.find_all('div', class_=re.compile('content|article|post|entry')):
            div_text = div.get_text().strip()
            if div_text and len(div_text) > 50:
                divs.append(div_text[:1000])
        
        text_content = soup.get_text()
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'url': url,
            'title': title_text,
            'headings': headings,
            'paragraphs': paragraphs,
            'lists': lists,
            'divs': divs,
            'full_text': clean_text[:10000],
            'scraped_at': datetime.now().isoformat()
        }
    
    def _extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(current_url, href)
            normalized_url = self.normalize_url(absolute_url)
            
            if self.is_valid_url(normalized_url) and normalized_url not in self.visited_urls:
                links.append(normalized_url)
        
        for button in soup.find_all(['button', 'div', 'span'], attrs={'onclick': True}):
            onclick = button.get('onclick', '')
            url_match = re.search(r'["\']([^"\']+)["\']', onclick)
            if url_match:
                href = url_match.group(1)
                absolute_url = urljoin(current_url, href)
                normalized_url = self.normalize_url(absolute_url)
                if self.is_valid_url(normalized_url) and normalized_url not in self.visited_urls:
                    links.append(normalized_url)
        
        for area in soup.find_all('area', href=True):
            href = area['href']
            absolute_url = urljoin(current_url, href)
            normalized_url = self.normalize_url(absolute_url)
            if self.is_valid_url(normalized_url) and normalized_url not in self.visited_urls:
                links.append(normalized_url)
        
        try:
            js_links = self.driver.execute_script("""
                var links = [];
                var elements = document.querySelectorAll('[href], [data-href], [data-url]');
                elements.forEach(function(el) {
                    var href = el.getAttribute('href') || el.getAttribute('data-href') || el.getAttribute('data-url');
                    if (href) links.push(href);
                });
                return links;
            """)
            for href in js_links:
                if href and not href.startswith('javascript:'):
                    absolute_url = urljoin(current_url, href)
                    normalized_url = self.normalize_url(absolute_url)
                    if self.is_valid_url(normalized_url) and normalized_url not in self.visited_urls:
                        links.append(normalized_url)
        except:
            pass
        
        return list(set(links))
    
    def classify_category(self, url: str, page_data: Dict[str, Any]) -> str:
        url_lower = url.lower()
        title_lower = page_data['title'].lower()
        text_lower = page_data['full_text'].lower()[:500]
        
        if any(kw in url_lower or kw in title_lower for kw in ['admission', 'apply', 'application', 'entrance']):
            return 'admission'
        elif any(kw in url_lower or kw in title_lower for kw in ['registration', 'register', 'enroll']):
            return 'registration'
        elif any(kw in url_lower or kw in title_lower for kw in ['fee', 'payment', 'tuition', 'cost']):
            return 'fees'
        elif any(kw in url_lower or kw in title_lower for kw in ['transcript', 'certificate', 'document', 'diploma']):
            return 'documents'
        elif any(kw in url_lower or kw in title_lower for kw in ['grade', 'result', 'score', 'gpa', 'exam']):
            return 'grades'
        elif any(kw in url_lower or kw in title_lower for kw in ['course', 'curriculum', 'program', 'department', 'faculty']):
            return 'courses'
        elif any(kw in url_lower or kw in title_lower for kw in ['event', 'calendar', 'schedule']):
            return 'events'
        elif any(kw in url_lower or kw in title_lower for kw in ['news', 'announcement', 'update']):
            return 'news'
        elif any(kw in url_lower or kw in title_lower for kw in ['research', 'publication', 'journal']):
            return 'research'
        elif any(kw in url_lower or kw in title_lower for kw in ['library', 'book', 'resource']):
            return 'library'
        else:
            return 'general'
    
    def crawl_website(self):
        logger.info(f"Starting crawl of {self.base_url}")
        
        self.setup_driver()
        
        try:
            self.to_visit.append(self.base_url)
            
            common_pages = [
                '/', '/about', '/admission', '/admissions', '/academics', '/programs',
                '/departments', '/colleges', '/faculties', '/registration', '/student-services',
                '/academic-services', '/fees', '/tuition', '/library', '/research', '/contact',
                '/news', '/events', '/undergraduate', '/graduate', '/postgraduate', '/campus',
                '/announcements', '/publications', '/gallery', '/services', '/partners', '/staffs',
                '/statistics', '/studentsCorner', '/alumni', '/campus_life', '/staff-profile'
            ]
            
            for page in common_pages:
                full_url = urljoin(self.base_url, page)
                if full_url not in self.visited_urls:
                    self.to_visit.append(full_url)
            
            page_patterns = [
                '/pages/Admission/', '/pages/Library/', '/pages/AAU-Services/',
                '/pages/Research/', '/pages/Academic/', '/pages/Student/',
                '/news/detail?title=', '/announcements/detail?title=',
                '/gallery/', '/publications/'
            ]
            
            while self.to_visit and len(self.visited_urls) < self.max_pages:
                current_url = self.to_visit.popleft()
                
                if current_url in self.visited_urls:
                    continue
                
                logger.info(f"[{len(self.visited_urls) + 1}/{self.max_pages}]: {current_url}")
                
                result = self.crawl_page(current_url)
                self.visited_urls.add(current_url)
                
                if result['page_data']:
                    category = self.classify_category(current_url, result['page_data'])
                    self.scraped_by_category[category].append(result['page_data'])
                    logger.info(f"Categorized as: {category}")
                
                for link in result['links']:
                    if link not in self.visited_urls and link not in self.to_visit:
                        self.to_visit.append(link)
                
                if len(self.to_visit) < 5 and len(self.visited_urls) < self.max_pages:
                    for pattern in page_patterns:
                        if pattern in current_url:
                            base_pattern = current_url.split(pattern)[0] + pattern
                            for i in range(1, 20):
                                test_url = f"{base_pattern}{i}"
                                if test_url not in self.visited_urls and test_url not in self.to_visit:
                                    self.to_visit.append(test_url)
                
                logger.info(f"Queue: {len(self.to_visit)}, Visited: {len(self.visited_urls)}")
            
            logger.info(f"Crawling completed. Visited {len(self.visited_urls)} pages")
            
        finally:
            self.close_driver()
    
    def save_by_category(self):
        output_dir = Path('data/raw/categories')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for category, data in self.scraped_by_category.items():
            if data:
                filename = f'aau_{category}.json'
                filepath = output_dir / filename
                
                existing_data = []
                if filepath.exists():
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            existing_data = json.load(f)
                    except:
                        pass
                
                existing_urls = {item['url'] for item in existing_data if 'url' in item}
                new_data = [item for item in data if item['url'] not in existing_urls]
                
                combined_data = existing_data + new_data
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(combined_data, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Saved {len(combined_data)} items ({len(new_data)} new) to {filename}")
    
    def save_stats(self):
        stats = {
            'total_pages_visited': len(self.visited_urls),
            'pages_by_category': {cat: len(data) for cat, data in self.scraped_by_category.items()},
            'visited_urls': list(self.visited_urls),
            'crawl_completed_at': datetime.now().isoformat(),
            'base_url': self.base_url
        }
        
        output_path = Path('data/raw/crawl_statistics.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved statistics")
    
    def run_scraping(self):
        logger.info("=" * 80)
        logger.info(f"AAU Website Scraping - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        
        self.crawl_website()
        self.save_by_category()
        self.save_stats()
        
        logger.info("=" * 80)
        logger.info("SCRAPING COMPLETED")
        for category, data in self.scraped_by_category.items():
            if data:
                logger.info(f"  {category}: {len(data)} pages")
        logger.info("=" * 80)

def run_periodic_scraping():
    scraper = AAUWebScraper()
    scraper.run_scraping()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        logger.info("Starting continuous scraping mode")
        logger.info("Scraping every 24 hours")
        
        run_periodic_scraping()
        
        schedule.every(24).hours.do(run_periodic_scraping)
        
        while True:
            schedule.run_pending()
            time.sleep(3600)
    else:
        run_periodic_scraping()
