"""
Command line interface for the News Agent
"""

import os
import argparse
from ..core.agent import NewsAgent


def main():
    """Main function to run the news agent"""
    parser = argparse.ArgumentParser(description='News Agent - Download latest news and generate web page')
    parser.add_argument('topic', help='News topic to search for')
    parser.add_argument('--articles', '-a', type=int, default=10, help='Number of articles to fetch (default: 10)')
    parser.add_argument('--output', '-o', help='Output filename (default: auto-generated)')
    parser.add_argument('--no-high-res', action='store_true', help='Disable high-resolution image search (faster but lower quality)')
    parser.add_argument('--no-download', action='store_true', help='Disable local image downloading (use remote URLs)')
    
    args = parser.parse_args()
    
    try:
        # Initialize and run the news agent
        agent = NewsAgent(high_res_images=not args.no_high_res, download_images=not args.no_download)
        filepath = agent.run(args.topic, args.articles, args.output)
        
        if filepath:
            print(f"\n🌐 Open the generated page in your browser:")
            print(f"   file://{os.path.abspath(filepath)}")
        
    except Exception as e:
        print(f"❌ Error running News Agent: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
