# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

News Agent is a news aggregation and analysis tool that:
1. Fetches latest news on any topic via SerpAPI
2. Searches for high-resolution images for each article
3. Generates AI-powered summaries using Google Gemini
4. Creates responsive HTML pages with the aggregated content
5. Optionally downloads and manages local images with automatic cleanup

## Required Environment Variables

Set these in `set_env.sh`:
- `SERPAPI_API_KEY`: SerpAPI key for news and image search
- `GOOGLE_API_KEY`: Google API key for Gemini AI summarization
- `LANGSMITH_API_KEY` (optional): For LangSmith tracing

Load environment variables before running:
```bash
source set_env.sh
```

## Common Commands

### Setup and Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install as package (for console script)
pip install -e .
```

### Running the Application
```bash
# Main script (recommended)
python news_agent.py "topic" --articles 10 --output filename.html

# As Python module
python -m news_agent.cli.main "topic" --articles 10 --output filename.html

# As installed console script
news-agent "topic" --articles 10

# Options:
# --articles, -a: Number of articles (default: 10)
# --output, -o: Output filename
# --no-high-res: Skip high-res image search (faster)
# --no-download: Don't download images locally
```

### Programmatic Usage
```python
from news_agent import NewsAgent

agent = NewsAgent(high_res_images=True, download_images=True)
filepath = agent.run("topic", num_articles=10, output_file="custom.html")
```

## Architecture

The project follows a modular component-based architecture:

### Core Components (news_agent/core/)

1. **NewsAgent** (agent.py): Main coordinator that orchestrates the workflow
   - Initializes all components with API keys from Settings
   - Executes pipeline: fetch news → search images → generate summary → create HTML
   - Handles image cleanup based on age

2. **NewsSearcher** (search.py): News search via SerpAPI
   - Uses `tbm=nws` for news-specific results
   - Filters by date (`tbs=qdr:d` for past day)
   - Returns structured articles with title, link, snippet, date, source, and image URLs

3. **ImageHandler** (image_handler.py): Multi-stage image handling
   - Searches for high-res images using SerpAPI image search (`tbm=isch`)
   - Falls back to article thumbnails if high-res search fails
   - Downloads images locally with MD5-based filenames to avoid duplicates
   - Cleans up images older than specified days (default: 7)

4. **AISummarizer** (ai_summarizer.py): Google Gemini integration
   - Uses LangChain with Google Generative AI
   - Generates comprehensive news summaries from article collection

5. **WebGenerator** (web_generator.py): HTML page creation
   - Generates responsive, modern HTML pages
   - Integrates with ImageHandler to get best available image URLs
   - Auto-generates timestamped filenames if not specified

### Configuration (news_agent/config/)

**Settings** (settings.py): Centralized configuration
- Validates required API keys on initialization
- Manages image directory path and retention policy
- Raises ValueError if required keys are missing

### Key Design Patterns

1. **Dependency Injection**: Components receive dependencies (API keys, settings) via constructor
2. **Separation of Concerns**: Each component handles a single responsibility
3. **Graceful Degradation**: Falls back to lower quality images if high-res search fails
4. **Resource Management**: Automatic cleanup of old images to prevent disk bloat

### Data Flow

```
User Input (topic, num_articles)
  ↓
NewsAgent.run()
  ↓
NewsSearcher.fetch_news() → List[Dict] with article metadata
  ↓
ImageHandler.get_best_image_url() → High-res image URL or fallback
  ↓
AISummarizer.generate_news_summary() → AI-generated summary
  ↓
WebGenerator.generate_html_page() → HTML content
  ↓
WebGenerator.save_web_page() → Saved HTML file path
```

### Image Resolution Strategy

The ImageHandler uses a three-tier approach:
1. High-res search via SerpAPI image search (if enabled)
2. Original article image/thumbnail from news results
3. Empty string if no images available

When downloading is enabled, images are saved with hash-based filenames to prevent duplicates.

## Package Structure

```
news_agent/
├── core/           # Main business logic
├── config/         # Settings and configuration
├── cli/            # Command-line interface
└── utils/          # Utility functions (currently minimal)
```

Entry points:
- Main script: `python news_agent.py`
- Console script: `news-agent` (defined in setup.py)
- CLI module: `python -m news_agent.cli.main`
