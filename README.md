# News Agent

A news aggregation and analysis tool that fetches the latest news on any topic and generates beautiful, interactive web pages with AI-powered summaries and high-resolution images.

## Live Demo

**🌐 [View Latest AI News](https://roberto-delfiore.github.io/news_agent/)**

Automatically generated daily with the latest artificial intelligence news.

## Project Structure

```
news_agent/
├── news_agent/                 # Main package
│   ├── __init__.py            # Package initialization
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── agent.py           # Main NewsAgent class
│   │   ├── search.py          # News search functionality
│   │   ├── image_handler.py   # Image search and download
│   │   ├── ai_summarizer.py   # AI-powered summarization
│   │   └── web_generator.py   # HTML page generation
│   ├── config/                # Configuration
│   │   ├── __init__.py
│   │   └── settings.py        # Settings and validation
│   ├── utils/                 # Utility functions
│   │   └── __init__.py
│   └── cli/                   # Command line interface
│       ├── __init__.py
│       └── main.py            # CLI entry point
├── news_agent.py              # Main CLI script
├── requirements.txt           # Dependencies
├── set_env.sh.template       # Environment variables template
└── README.md                 # This file
```

## Features

- 🔍 **Smart News Search**: Uses SerpAPI to fetch the latest news on any topic
- 🤖 **AI-Powered Analysis**: Google Gemini generates comprehensive summaries
- 🖼️ **High-Resolution Images**: Automatically searches for and downloads high-quality images
- 🌐 **Beautiful Web Pages**: Generates responsive, modern HTML pages
- 📥 **Local Image Storage**: Optional local image downloading and management
- 🧹 **Automatic Cleanup**: Removes old images to save disk space
- ⚡ **Fast Performance**: Optimized for speed with configurable quality settings

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/roberto-delfiore/news_agent.git
cd news_agent
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Copy the environment template and add your API keys:

```bash
cp set_env.sh.template set_env.sh
```

Edit `set_env.sh` and add your API keys:

- **SERPAPI_API_KEY**: Get from [SerpAPI](https://serpapi.com/) (required for news and image search)
- **GOOGLE_API_KEY**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey) (required for AI summaries)
- **LANGSMITH_API_KEY**: Optional - Get from [LangSmith](https://smith.langchain.com/) for tracing

### 5. Load Environment Variables
```bash
source set_env.sh
```

**Note**: The `set_env.sh` file contains your private API keys and is ignored by git. Never commit this file to version control.

## Usage

### Main Script (Recommended)
```bash
python news_agent.py "artificial intelligence" --articles 15 --output ai_news.html
```

### As Python Module
```bash
python -m news_agent.cli.main "artificial intelligence" --articles 15 --output ai_news.html
```

### As a Python Package
```python
from news_agent import NewsAgent

agent = NewsAgent(high_res_images=True, download_images=True)
filepath = agent.run("climate change", num_articles=10)
print(f"Generated: {filepath}")
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `topic` | - | News topic to search for | Required |
| `--articles` | `-a` | Number of articles to fetch | 10 |
| `--output` | `-o` | Output filename | Auto-generated |
| `--no-high-res` | - | Disable high-resolution image search (faster) | Enabled |
| `--no-download` | - | Disable local image downloading | Enabled |

## Examples

```bash
# Basic usage
python news_agent.py "quantum computing"

# Advanced usage
python news_agent.py "space exploration" --articles 20 --output space_news.html --no-download

# Fast mode (no high-res images)
python news_agent.py "cryptocurrency" --no-high-res

# Get help
python news_agent.py --help
```

## Dependencies

- `langchain==0.3.25` - LLM framework
- `langchain-community==0.3.25` - Community components
- `langchain-google-genai==2.1.5` - Google Gemini integration
- `beautifulsoup4` - HTML parsing
- `google-search-results` - SerpAPI client
- `requests` - HTTP requests

## Architecture

The project follows a modular architecture:

- **Agent**: Main coordinator class
- **Search**: Handles news fetching via SerpAPI
- **ImageHandler**: Manages image search, download, and cleanup
- **AISummarizer**: Generates AI-powered summaries using Gemini
- **WebGenerator**: Creates beautiful HTML pages
- **Settings**: Manages configuration and validation

This design makes the code maintainable, testable, and extensible.

## Output

The tool generates:
- **HTML Pages**: Responsive web pages with news articles, images, and AI summaries (saved as `news_page_YYYYMMDD_HHMMSS.html`)
- **Downloaded Images**: High-resolution images stored in `news_images/` directory (optional)
- **Auto Cleanup**: Images older than 7 days are automatically removed

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Troubleshooting

### API Key Issues
If you see errors about missing API keys:
1. Ensure `set_env.sh` exists and contains your keys
2. Run `source set_env.sh` in your terminal
3. Verify keys are loaded: `echo $SERPAPI_API_KEY`

### Image Download Issues
- Use `--no-download` flag to skip local image storage
- Use `--no-high-res` for faster execution with lower quality images

### Rate Limiting
If you hit API rate limits, reduce the number of articles or add delays between requests. 