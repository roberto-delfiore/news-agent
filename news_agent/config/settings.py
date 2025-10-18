"""
Configuration settings for the News Agent
"""

import os
from typing import Optional


class Settings:
    """Configuration settings for the News Agent"""
    
    def __init__(self):
        self.serpapi_key: Optional[str] = os.getenv('SERPAPI_API_KEY')
        self.google_api_key: Optional[str] = os.getenv('GOOGLE_API_KEY')
        self.images_dir: str = os.path.join(os.getcwd(), 'news_images')
        self.keep_images_days: int = 7
        
    def validate(self) -> None:
        """Validate that required API keys are present"""
        if not self.serpapi_key:
            raise ValueError("SERPAPI_API_KEY environment variable is required")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
