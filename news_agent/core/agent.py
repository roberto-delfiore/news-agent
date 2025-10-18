"""
Main NewsAgent class that coordinates all functionality
"""

from typing import List, Dict, Any, Optional

from .search import NewsSearcher
from .image_handler import ImageHandler
from .ai_summarizer import AISummarizer
from .web_generator import WebGenerator
from ..config.settings import Settings


class NewsAgent:
    """Main agent that fetches news and generates web pages"""
    
    def __init__(self, high_res_images: bool = True, download_images: bool = True):
        """Initialize the news agent with API keys"""
        self.settings = Settings()
        self.settings.validate()
        
        self.high_res_images = high_res_images
        self.download_images = download_images
        
        # Initialize components
        self.searcher = NewsSearcher(self.settings.serpapi_key)
        self.image_handler = ImageHandler(
            self.settings.serpapi_key, 
            download_images, 
            high_res_images
        )
        self.ai_summarizer = AISummarizer(self.settings.google_api_key)
        self.web_generator = WebGenerator(self.image_handler)
    
    def run(self, topic: str, num_articles: int = 10, output_file: Optional[str] = None) -> str:
        """
        Main method to run the news agent
        
        Args:
            topic: News topic to search for
            num_articles: Number of articles to fetch
            output_file: Optional output filename
            
        Returns:
            Path to the generated web page
        """
        print(f"🚀 Starting News Agent for topic: '{topic}'")
        print("=" * 50)
        
        # Clean up old images if downloading is enabled
        if self.download_images:
            self.image_handler.cleanup_old_images(self.settings.keep_images_days)
        
        # Fetch news articles
        news_articles = self.searcher.fetch_news(topic, num_articles)
        
        # Generate AI summary
        print("🤖 Generating AI summary...")
        summary = self.ai_summarizer.generate_news_summary(topic, news_articles)
        
        # Generate HTML page
        print("🌐 Generating web page...")
        html_content = self.web_generator.generate_html_page(topic, news_articles, summary)
        
        # Save the page
        filepath = self.web_generator.save_web_page(html_content, output_file)
        
        print("=" * 50)
        print(f"✅ News Agent completed successfully!")
        print(f"📄 Generated page: {filepath}")
        print(f"📊 Found {len(news_articles)} articles")
        
        return filepath
