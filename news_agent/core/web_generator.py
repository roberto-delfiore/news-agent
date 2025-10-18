"""
Web page generation functionality for the News Agent
"""

import os
from datetime import datetime
from typing import List, Dict, Any


class WebGenerator:
    """Handles HTML page generation"""
    
    def __init__(self, image_handler):
        self.image_handler = image_handler
    
    def generate_html_page(self, topic: str, news_articles: List[Dict[str, Any]], summary: str) -> str:
        """
        Generate an HTML page with the news content
        
        Args:
            topic: The news topic
            news_articles: List of news articles
            summary: AI-generated summary
            
        Returns:
            HTML content as string
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Latest News: {topic}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .timestamp {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin-bottom: 30px;
        }}
        .summary {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 5px solid #3498db;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .summary h2 {{
            color: #2c3e50;
            margin-top: 0;
            margin-bottom: 20px;
            font-size: 1.4em;
            display: flex;
            align-items: center;
        }}
        .summary h2::before {{
            content: "📊";
            margin-right: 10px;
            font-size: 1.2em;
        }}
        .summary h3 {{
            color: #2980b9;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.1em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }}
        .summary ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .summary li {{
            margin-bottom: 8px;
            line-height: 1.5;
        }}
        .summary strong {{
            color: #2c3e50;
            font-weight: 600;
        }}
        .summary p {{
            margin-bottom: 15px;
            line-height: 1.6;
        }}
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .news-item {{
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
            overflow: hidden;
        }}
        .news-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .news-image {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 15px;
            background-color: #f8f9fa;
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
            image-rendering: high-quality;
            filter: contrast(1.1) saturate(1.1);
            transition: transform 0.3s ease;
        }}
        .news-image:hover {{
            transform: scale(1.02);
        }}
        .news-image-placeholder {{
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 6px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2em;
            font-weight: bold;
        }}
        .news-title {{
            color: #2c3e50;
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .news-title a {{
            color: #2c3e50;
            text-decoration: none;
        }}
        .news-title a:hover {{
            color: #3498db;
        }}
        .news-source {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 8px;
        }}
        .news-date {{
            color: #95a5a6;
            font-size: 0.8em;
            margin-bottom: 10px;
        }}
        .news-snippet {{
            color: #34495e;
            line-height: 1.5;
        }}
        .no-news {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            padding: 40px;
        }}
        /* Image quality improvements */
        .news-image {{
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
        }}
        /* Better image rendering for high DPI displays */
        @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
            .news-image {{
                image-rendering: -webkit-optimize-contrast;
                image-rendering: crisp-edges;
            }}
        }}
    </style>
    <script>
        // Image quality enhancement script
        document.addEventListener('DOMContentLoaded', function() {{
            const images = document.querySelectorAll('.news-image');
            images.forEach(img => {{
                // Force high quality rendering
                img.style.imageRendering = 'high-quality';
                img.style.imageRendering = '-webkit-optimize-contrast';
                
                // Add error handling for better fallback
                img.addEventListener('error', function() {{
                    this.style.display = 'none';
                    const placeholder = this.nextElementSibling;
                    if (placeholder && placeholder.classList.contains('news-image-placeholder')) {{
                        placeholder.style.display = 'flex';
                    }}
                }});
                
                // Add load event for smooth transition
                img.addEventListener('load', function() {{
                    this.style.opacity = '1';
                }});
            }});
        }});
    </script>
</head>
<body>
    <div class="container">
        <h1>📰 Latest News: {topic}</h1>
        <div class="timestamp">Last updated: {current_time}</div>
        
        <div class="summary">
            <h2>News Analysis</h2>
            {summary}
        </div>
        
        <h2>📋 Recent Articles</h2>
        <div class="news-grid">
"""
        
        if news_articles:
            for article in news_articles:
                # Get the best quality image URL
                image_url = self.image_handler.get_best_image_url(article)
                
                # Create image HTML with better error handling and quality optimization
                if image_url:
                    # Convert absolute path to relative path for local images
                    if os.path.isabs(image_url) and self.image_handler.download_images:
                        # Get relative path from current directory
                        rel_path = os.path.relpath(image_url, os.getcwd())
                        image_src = rel_path
                    else:
                        image_src = image_url
                    
                    # Add loading="lazy" for better performance and srcset for responsive images
                    image_html = f'''<img src="{image_src}" 
                        alt="{article["title"]}" 
                        class="news-image" 
                        loading="lazy"
                        onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                        onload="this.style.opacity='1';"
                        style="opacity:0; transition: opacity 0.3s ease;">'''
                    placeholder_html = f'<div class="news-image-placeholder" style="display:none;">📰 {article["source"]}</div>'
                else:
                    image_html = ''
                    placeholder_html = f'<div class="news-image-placeholder">📰 {article["source"]}</div>'
                
                html_content += f"""
            <div class="news-item">
                {image_html}
                {placeholder_html}
                <div class="news-title">
                    <a href="{article['link']}" target="_blank">{article['title']}</a>
                </div>
                <div class="news-source">Source: {article['source']}</div>
                <div class="news-date">Date: {article['date']}</div>
                <div class="news-snippet">{article['snippet']}</div>
            </div>
"""
        else:
            html_content += """
            <div class="no-news">
                <p>No recent news articles found for this topic.</p>
            </div>
"""
        
        html_content += """
        </div>
    </div>
</body>
</html>
"""
        
        return html_content
    
    def save_web_page(self, html_content: str, filename: str = None) -> str:
        """
        Save the HTML content to a file
        
        Args:
            html_content: HTML content to save
            filename: Optional custom filename
            
        Returns:
            Path to the saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_page_{timestamp}.html"
        
        filepath = os.path.join(os.getcwd(), filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Web page saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving web page: {e}")
            return ""
