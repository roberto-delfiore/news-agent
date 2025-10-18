#!/usr/bin/env python3
"""
Command-line script to run the News Agent
"""

import os
import sys
import argparse
from news_agent import NewsAgent


def main():
    """News agent CLI runner"""
    parser = argparse.ArgumentParser(
        description="News Agent - Fetch and analyze news on any topic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "artificial intelligence" --articles 15
  %(prog)s "climate change" -a 20 -o climate_news.html
  %(prog)s "space exploration" --no-high-res --no-download
        """
    )

    parser.add_argument(
        "topic",
        help="News topic to search for"
    )

    parser.add_argument(
        "-a", "--articles",
        type=int,
        default=10,
        help="Number of articles to fetch (default: 10)"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output filename (default: auto-generated with timestamp)"
    )

    parser.add_argument(
        "--no-high-res",
        action="store_true",
        help="Disable high-resolution image search (faster)"
    )

    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Don't download images locally (use remote URLs)"
    )

    args = parser.parse_args()

    # Check environment variables
    if not os.getenv('SERPAPI_API_KEY') or not os.getenv('GOOGLE_API_KEY'):
        print("❌ Error: Missing required API keys")
        print("   Please set SERPAPI_API_KEY and GOOGLE_API_KEY environment variables")
        print("   Run: source set_env.sh")
        return 1

    try:
        # Initialize agent with settings
        high_res_images = not args.no_high_res
        download_images = not args.no_download

        agent = NewsAgent(
            high_res_images=high_res_images,
            download_images=download_images
        )

        # Run the agent
        filepath = agent.run(args.topic, args.articles, args.output)

        if filepath:
            print(f"\n🌐 Open the generated page in your browser:")
            print(f"   file://{os.path.abspath(filepath)}")

        return 0

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
