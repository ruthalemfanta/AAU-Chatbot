"""Data processing and cleaning utilities."""
import re
import csv
from pathlib import Path
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Data cleaning and normalization processor."""
    
    def __init__(self):
        """Initialize the data processor."""
        # Common misspellings (can be expanded)
        self.common_corrections = {
            'admission': ['admission', 'admission'],
            'registration': ['registration', 'registraion'],
            'transcript': ['transcript', 'transcrip'],
        }
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text: lowercase, remove extra spaces.
        
        Args:
            text: Input text
            
        Returns:
            str: Normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def clean_text(self, text: str, keep_punctuation: bool = True) -> str:
        """
        Clean text: remove special characters, normalize.
        
        Args:
            text: Input text
            keep_punctuation: Whether to keep essential punctuation
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Normalize first
        text = self.normalize_text(text)
        
        if keep_punctuation:
            # Keep essential punctuation: . ? ! , : ; - ( )
            # Remove other special characters
            text = re.sub(r'[^\w\s\.\?\!\,\:\;\-\(\)]', '', text)
        else:
            # Remove all punctuation
            text = re.sub(r'[^\w\s]', '', text)
        
        # Remove extra spaces again after cleaning
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def detect_language(self, text: str) -> str:
        """
        Simple language detection (English vs Amharic).
        
        Args:
            text: Input text
            
        Returns:
            str: 'en' for English, 'am' for Amharic, 'mixed' for mixed
        """
        if not text:
            return 'unknown'
        
        # Amharic Unicode range: U+1200 to U+137F
        amharic_pattern = re.compile(r'[\u1200-\u137F]')
        has_amharic = bool(amharic_pattern.search(text))
        
        # Check for English characters
        english_pattern = re.compile(r'[a-zA-Z]')
        has_english = bool(english_pattern.search(text))
        
        if has_amharic and has_english:
            return 'mixed'
        elif has_amharic:
            return 'am'
        elif has_english:
            return 'en'
        else:
            return 'unknown'
    
    def remove_duplicates(self, texts: List[str]) -> List[str]:
        """
        Remove duplicate texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List[str]: List with duplicates removed
        """
        seen = set()
        unique_texts = []
        
        for text in texts:
            # Normalize for comparison
            normalized = self.normalize_text(text)
            if normalized not in seen and len(normalized) > 5:  # Minimum length
                seen.add(normalized)
                unique_texts.append(text)
        
        return unique_texts
    
    def process_csv(self, input_path: Path, output_path: Path):
        """
        Process a CSV file: clean and normalize all text fields.
        
        Args:
            input_path: Path to input CSV file
            output_path: Path to output CSV file
        """
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        if not input_path.exists():
            logger.error(f"Input file not found: {input_path}")
            return
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Processing {input_path} -> {output_path}")
        
        processed_rows = []
        raw_texts = []
        
        # Read and process
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            for row in reader:
                raw_text = row.get('raw_text', '')
                raw_texts.append(raw_text)
                
                # Clean the text
                cleaned_text = self.clean_text(raw_text, keep_punctuation=True)
                
                # Update row
                row['cleaned_text'] = cleaned_text
                
                # Add language detection if 'language' column doesn't exist
                if 'language' not in row:
                    row['language'] = self.detect_language(raw_text)
                
                processed_rows.append(row)
        
        # Remove duplicates based on cleaned_text
        logger.info(f"Removing duplicates from {len(processed_rows)} rows...")
        seen_cleaned = set()
        unique_rows = []
        
        for row in processed_rows:
            cleaned = row.get('cleaned_text', '')
            if cleaned not in seen_cleaned and len(cleaned) > 5:
                seen_cleaned.add(cleaned)
                unique_rows.append(row)
        
        logger.info(f"After deduplication: {len(unique_rows)} rows")
        
        # Write processed data
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if unique_rows:
                # Add 'language' to fieldnames if not present
                fieldnames = list(unique_rows[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(unique_rows)
        
        logger.info(f"Processed data saved to {output_path}")
        logger.info(f"Total rows: {len(unique_rows)}")
        
        return len(unique_rows)


def process_collected_data():
    """Main function to process collected data."""
    processor = DataProcessor()
    
    input_path = Path("data/raw/collected_data.csv")
    output_path = Path("data/processed/cleaned_data.csv")
    
    if not input_path.exists():
        logger.warning(f"Input file not found: {input_path}")
        logger.info("Run web_scrapper.py or telegram_cli.py first to collect data")
        return
    
    row_count = processor.process_csv(input_path, output_path)
    
    print(f"\nData processing complete!")
    print(f"Processed {row_count} rows")
    print(f"Cleaned data saved to: {output_path}")


if __name__ == "__main__":
    process_collected_data()