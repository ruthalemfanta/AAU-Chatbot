"""Generate statistics for collected data."""
import csv
from pathlib import Path
from collections import Counter
import statistics
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataStatistics:
    """Generate statistics from collected data."""
    
    def __init__(self, data_path: Path):
        """
        Initialize statistics generator.
        
        Args:
            data_path: Path to CSV data file
        """
        self.data_path = Path(data_path)
        self.data = []
        self.load_data()
    
    def load_data(self):
        """Load data from CSV file."""
        if not self.data_path.exists():
            logger.error(f"Data file not found: {self.data_path}")
            return
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
        
        logger.info(f"Loaded {len(self.data)} rows from {self.data_path}")
    
    def count_by_source(self) -> Dict[str, int]:
        """Count questions by source."""
        sources = Counter(row.get('source', 'unknown') for row in self.data)
        return dict(sources)
    
    def text_length_stats(self) -> Dict[str, float]:
        """Calculate text length statistics."""
        lengths = []
        cleaned_lengths = []
        
        for row in self.data:
            raw_text = row.get('raw_text', '')
            cleaned_text = row.get('cleaned_text', '')
            
            if raw_text:
                lengths.append(len(raw_text))
            if cleaned_text:
                cleaned_lengths.append(len(cleaned_text))
        
        stats = {}
        if lengths:
            stats['raw_text'] = {
                'mean': statistics.mean(lengths),
                'median': statistics.median(lengths),
                'min': min(lengths),
                'max': max(lengths),
                'count': len(lengths)
            }
        
        if cleaned_lengths:
            stats['cleaned_text'] = {
                'mean': statistics.mean(cleaned_lengths),
                'median': statistics.median(cleaned_lengths),
                'min': min(cleaned_lengths),
                'max': max(cleaned_lengths),
                'count': len(cleaned_lengths)
            }
        
        return stats
    
    def language_distribution(self) -> Dict[str, int]:
        """Get language distribution."""
        languages = Counter(row.get('language', 'unknown') for row in self.data)
        return dict(languages)
    
    def generate_report(self) -> str:
        """Generate a comprehensive statistics report."""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("DATA COLLECTION STATISTICS REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # Total count
        total_count = len(self.data)
        report_lines.append(f"Total Questions Collected: {total_count}")
        report_lines.append("")
        
        # Source distribution
        report_lines.append("Source Distribution:")
        report_lines.append("-" * 40)
        source_counts = self.count_by_source()
        for source, count in source_counts.items():
            percentage = (count / total_count * 100) if total_count > 0 else 0
            report_lines.append(f"  {source:15s}: {count:5d} ({percentage:5.1f}%)")
        report_lines.append("")
        
        # Text length statistics
        report_lines.append("Text Length Statistics:")
        report_lines.append("-" * 40)
        length_stats = self.text_length_stats()
        
        if 'raw_text' in length_stats:
            stats = length_stats['raw_text']
            report_lines.append("  Raw Text:")
            report_lines.append(f"    Mean:   {stats['mean']:.1f} characters")
            report_lines.append(f"    Median: {stats['median']:.1f} characters")
            report_lines.append(f"    Min:    {stats['min']} characters")
            report_lines.append(f"    Max:    {stats['max']} characters")
            report_lines.append(f"    Count:  {stats['count']}")
        
        if 'cleaned_text' in length_stats:
            stats = length_stats['cleaned_text']
            report_lines.append("  Cleaned Text:")
            report_lines.append(f"    Mean:   {stats['mean']:.1f} characters")
            report_lines.append(f"    Median: {stats['median']:.1f} characters")
            report_lines.append(f"    Min:    {stats['min']} characters")
            report_lines.append(f"    Max:    {stats['max']} characters")
            report_lines.append(f"    Count:  {stats['count']}")
        report_lines.append("")
        
        # Language distribution
        report_lines.append("Language Distribution:")
        report_lines.append("-" * 40)
        lang_dist = self.language_distribution()
        for lang, count in lang_dist.items():
            percentage = (count / total_count * 100) if total_count > 0 else 0
            report_lines.append(f"  {lang:15s}: {count:5d} ({percentage:5.1f}%)")
        report_lines.append("")
        
        # Page type distribution (if available)
        page_types = Counter(row.get('page_type', 'N/A') for row in self.data if row.get('page_type'))
        if page_types:
            report_lines.append("Page Type Distribution (Website):")
            report_lines.append("-" * 40)
            for page_type, count in page_types.items():
                percentage = (count / total_count * 100) if total_count > 0 else 0
                report_lines.append(f"  {page_type:20s}: {count:5d} ({percentage:5.1f}%)")
            report_lines.append("")
        
        # Channel distribution (if available)
        channels = Counter(row.get('channel_name', '') for row in self.data if row.get('channel_name'))
        if channels:
            report_lines.append("Channel Distribution (Telegram):")
            report_lines.append("-" * 40)
            for channel, count in channels.items():
                if channel:  # Skip empty
                    percentage = (count / total_count * 100) if total_count > 0 else 0
                    report_lines.append(f"  {channel:20s}: {count:5d} ({percentage:5.1f}%)")
            report_lines.append("")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def save_report(self, output_path: Path):
        """Save statistics report to file."""
        report = self.generate_report()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Statistics report saved to {output_path}")
        return report


def generate_statistics():
    """Main function to generate statistics."""
    web_processed = Path("data/processed/web_cleaned_data.csv")
    telegram_processed = Path("data/processed/telegram_cleaned_data.csv")
    web_raw = Path("data/raw/web_collected_data.csv")
    telegram_raw = Path("data/raw/telegram_collected_data.csv")
    
    reports = []
    
    if web_processed.exists():
        logger.info("Generating statistics for web data (processed)...")
        stats = DataStatistics(web_processed)
        report_path = Path("reports/web_data_statistics.txt")
        report = stats.save_report(report_path)
        reports.append(("Web Data (Processed)", report))
    elif web_raw.exists():
        logger.info("Generating statistics for web data (raw)...")
        stats = DataStatistics(web_raw)
        report_path = Path("reports/web_data_statistics.txt")
        report = stats.save_report(report_path)
        reports.append(("Web Data (Raw)", report))
    
    if telegram_processed.exists():
        logger.info("Generating statistics for Telegram data (processed)...")
        stats = DataStatistics(telegram_processed)
        report_path = Path("reports/telegram_data_statistics.txt")
        report = stats.save_report(report_path)
        reports.append(("Telegram Data (Processed)", report))
    elif telegram_raw.exists():
        logger.info("Generating statistics for Telegram data (raw)...")
        stats = DataStatistics(telegram_raw)
        report_path = Path("reports/telegram_data_statistics.txt")
        report = stats.save_report(report_path)
        reports.append(("Telegram Data (Raw)", report))
    
    if not reports:
        logger.error("No data files found. Run data collection scripts first.")
        return
    
    for title, report in reports:
        print(f"\n{'=' * 70}")
        print(f"{title} Statistics")
        print('=' * 70)
        print(report)


if __name__ == "__main__":
    generate_statistics()
