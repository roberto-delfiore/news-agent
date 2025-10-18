"""
AI-powered news summarization functionality
"""

from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI


class AISummarizer:
    """Handles AI-powered news summarization using Google Gemini"""
    
    def __init__(self, google_api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=google_api_key,
            temperature=0.7
        )
    
    def generate_news_summary(self, topic: str, news_articles: List[Dict[str, Any]]) -> str:
        """
        Generate a summary of the news using AI
        
        Args:
            topic: The news topic
            news_articles: List of news articles
            
        Returns:
            AI-generated summary of the news
        """
        if not news_articles:
            return f"No recent news found about {topic}."
        
        # Prepare news content for AI processing
        news_content = f"Topic: {topic}\n\nRecent News Articles:\n\n"
        for i, article in enumerate(news_articles, 1):
            news_content += f"{i}. {article['title']}\n"
            news_content += f"   Source: {article['source']}\n"
            news_content += f"   Summary: {article['snippet']}\n"
            news_content += f"   Date: {article['date']}\n\n"
        
        system_prompt = """You are a news analyst. Analyze the provided news articles and create a comprehensive summary with the following structure:

**FORMAT REQUIREMENTS:**
- Use HTML formatting for better presentation
- Start with a brief 2-3 sentence overview
- Include 3-4 key bullet points using <ul><li> tags
- Add a "Key Insights" section with <h3> tags
- Use <strong> tags for important terms and numbers
- Keep it engaging and professional
- Total length: 200-300 words

**CONTENT REQUIREMENTS:**
1. Identify main themes and trends
2. Highlight most important developments with specific details
3. Provide context and analysis
4. Include relevant statistics or numbers when available
5. Focus on actionable insights rather than just repeating headlines

**EXAMPLE FORMAT:**
<p>Brief overview paragraph...</p>
<h3>Key Developments:</h3>
<ul>
<li><strong>Important point 1</strong> - with context</li>
<li><strong>Important point 2</strong> - with details</li>
</ul>
<h3>Key Insights:</h3>
<p>Analysis and implications...</p>"""
        
        try:
            # Create a single prompt with system and user content
            full_prompt = f"{system_prompt}\n\n{news_content}"
            
            print(f"🤖 Calling Gemini API with prompt length: {len(full_prompt)} characters")
            response = self.llm.invoke(full_prompt)
            print(f"✅ Received response from Gemini API")
            return response.content
            
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            print(f"   Error type: {type(e).__name__}")
            # Try alternative approach with simple prompt
            try:
                simple_prompt = f"Analyze these news articles about {topic} and provide a 200-word summary:\n\n{news_content}"
                response = self.llm.invoke(simple_prompt)
                return response.content
            except Exception as e2:
                print(f"❌ Alternative approach also failed: {e2}")
                return f"Summary generation failed. Found {len(news_articles)} articles about {topic}. Error: {str(e)}"
