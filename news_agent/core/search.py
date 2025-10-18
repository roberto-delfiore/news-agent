"""
News search functionality for the News Agent
"""

import requests
from typing import List, Dict, Any


class NewsSearcher:
    """Handles news search using SerpAPI"""
    
    def __init__(self, serpapi_key: str):
        self.serpapi_key = serpapi_key
    
    def fetch_news(self, topic: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch latest news about a specific topic using SerpAPI
        
        Args:
            topic: The news topic to search for
            num_results: Number of news articles to fetch
            
        Returns:
            List of news articles with title, link, snippet, and date
        """
        print(f"🔍 Fetching latest news about: {topic}")
        
        # SerpAPI parameters for news search with better image support
        params = {
            'q': f"{topic} news",
            'tbm': 'nws',  # News search
            'api_key': self.serpapi_key,
            'num': num_results,
            'sort': 'date',  # Sort by date
            'tbs': 'qdr:d',  # Past day
            'safe': 'active',  # Safe search
            'gl': 'us',  # Country
            'hl': 'en'  # Language
        }
        
        try:
            response = requests.get('https://serpapi.com/search', params=params)
            response.raise_for_status()
            
            data = response.json()
            news_results = data.get('news_results', [])
            
            # Process and clean the news results
            processed_news = []
            for article in news_results:
                processed_article = {
                    'title': article.get('title', 'No title'),
                    'link': article.get('link', ''),
                    'snippet': article.get('snippet', 'No description'),
                    'date': article.get('date', 'No date'),
                    'source': article.get('source', 'Unknown source'),
                    'image': article.get('image', ''),
                    'thumbnail': article.get('thumbnail', '')
                }
                processed_news.append(processed_article)
            
            print(f"✅ Found {len(processed_news)} news articles")
            return processed_news
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching news: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
