"""
Image handling functionality for the News Agent
"""

import os
import hashlib
import requests
import mimetypes
import time
from urllib.parse import urlparse
from typing import Dict, Any, Optional


class ImageHandler:
    """Handles image search, download, and management"""
    
    def __init__(self, serpapi_key: str, download_images: bool = True, high_res_images: bool = True):
        self.serpapi_key = serpapi_key
        self.download_images = download_images
        self.high_res_images = high_res_images
        self.images_dir = os.path.join(os.getcwd(), 'news_images')
        
        # Create images directory if it doesn't exist
        if self.download_images:
            os.makedirs(self.images_dir, exist_ok=True)
    
    def search_high_res_image(self, title: str, source: str) -> str:
        """
        Search for high resolution images based on article title and source
        
        Args:
            title: Article title
            source: News source
            
        Returns:
            High resolution image URL or empty string
        """
        try:
            # Create search query for images
            search_query = f"{title} {source}"
            
            # SerpAPI parameters for image search
            params = {
                'q': search_query,
                'tbm': 'isch',  # Image search
                'api_key': self.serpapi_key,
                'num': 3,  # Get top 3 results
                'safe': 'active',
                'gl': 'us',
                'hl': 'en',
                'ijn': 0  # First page
            }
            
            response = requests.get('https://serpapi.com/search', params=params)
            response.raise_for_status()
            
            data = response.json()
            images = data.get('images_results', [])
            
            # Look for high resolution images (prefer larger images)
            for img in images:
                img_url = img.get('original', '') or img.get('link', '')
                if img_url and isinstance(img_url, str) and img_url.startswith('http'):
                    # Check if image seems to be high resolution (not a small thumbnail)
                    if not any(size in img_url.lower() for size in ['92x92', '64x64', '48x48', '32x32']):
                        return img_url
            
            return ''
            
        except Exception as e:
            print(f"⚠️  Could not search for high-res image: {e}")
            return ''
    
    def download_image(self, image_url: str, article_title: str) -> str:
        """
        Download image and save it locally
        
        Args:
            image_url: URL of the image to download
            article_title: Title of the article (for filename)
            
        Returns:
            Local path to the downloaded image or empty string if failed
        """
        if not self.download_images:
            return image_url
        
        try:
            # Create a safe filename from the article title
            safe_title = "".join(c for c in article_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]  # Limit length
            
            # Get file extension from URL
            parsed_url = urlparse(image_url)
            path = parsed_url.path
            ext = os.path.splitext(path)[1]
            
            # If no extension, try to determine from content type
            if not ext:
                try:
                    response = requests.head(image_url, timeout=5)
                    content_type = response.headers.get('content-type', '')
                    ext = mimetypes.guess_extension(content_type) or '.jpg'
                except:
                    ext = '.jpg'
            
            # Create unique filename
            url_hash = hashlib.md5(image_url.encode()).hexdigest()[:8]
            filename = f"{safe_title}_{url_hash}{ext}"
            local_path = os.path.join(self.images_dir, filename)
            
            # Download the image
            print(f"📥 Downloading image: {filename}")
            response = requests.get(image_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Save the image
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Image saved: {filename}")
            return local_path
            
        except Exception as e:
            print(f"❌ Failed to download image: {e}")
            return image_url  # Return original URL as fallback
    
    def get_best_image_url(self, article: Dict[str, Any]) -> str:
        """
        Get the best quality image URL from available sources
        
        Args:
            article: News article dictionary
            
        Returns:
            Best available image URL
        """
        # First try to get high resolution image from image search
        title = article.get('title', '')
        source = article.get('source', '')
        
        # Get the best image URL (high-res or fallback)
        image_url = ''
        
        if title and source and self.high_res_images:
            print(f"🔍 Searching for high-res image: {title[:50]}...")
            high_res_image = self.search_high_res_image(title, source)
            if high_res_image:
                print(f"✅ Found high-res image: {high_res_image[:80]}...")
                image_url = high_res_image
            else:
                print(f"⚠️  No high-res image found, using fallback")
        
        # Fallback to original sources if no high-res image found
        if not image_url:
            image_sources = [
                article.get('image', ''),
                article.get('thumbnail', ''),
                article.get('image_url', ''),
                article.get('media', {}).get('image', '') if isinstance(article.get('media'), dict) else ''
            ]
            
            # Filter out empty strings and return the first valid URL
            for url in image_sources:
                if url and isinstance(url, str) and url.startswith('http'):
                    image_url = url
                    break
        
        # Download the image locally if we have a URL and download is enabled
        if image_url and self.download_images:
            return self.download_image(image_url, title)
        
        return image_url
    
    def cleanup_old_images(self, keep_days: int = 7):
        """
        Clean up old images to save disk space
        
        Args:
            keep_days: Number of days to keep images
        """
        if not os.path.exists(self.images_dir):
            return
        
        current_time = time.time()
        cutoff_time = current_time - (keep_days * 24 * 60 * 60)
        
        cleaned_count = 0
        for filename in os.listdir(self.images_dir):
            file_path = os.path.join(self.images_dir, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if file_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        cleaned_count += 1
                    except Exception as e:
                        print(f"⚠️  Could not remove old image {filename}: {e}")
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned up {cleaned_count} old images")
