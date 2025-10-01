"""
This module provides a client for interacting with the Crawl4AI library.

It encapsulates the logic for scraping a website using Crawl4AI and extracting
its content as a markdown string, handling potential errors during the process.
"""

from crawl4ai import AsyncWebCrawler


async def scrape_and_get_markdown_with_crawl4ai(url: str) -> str:
    """
    Asynchronously scrapes a given URL using Crawl4AI and returns its content as markdown.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The scraped content in markdown format. If scraping fails or returns
             no content, a formatted error message string is returned.
    """
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url) 

            markdown_content = "❌ <span style='color:red;'>Crawl4AI completed but returned no content. The page might be empty or inaccessible.</span>"

            if result and result.markdown:
                markdown_content = result.markdown
            
            return markdown_content
    except Exception as e:
        return f"❌ <span style='color:red;'>An error occurred while scraping with Crawl4AI: {e}</span>"