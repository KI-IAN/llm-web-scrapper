import asyncio
from crawl4ai import AsyncWebCrawler


async def scrape_and_get_markdown_with_crawl4ai(url: str) -> str:
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            if result and result.markdown:
                return result.markdown
            # If result is None or markdown is empty
            return "❌ <span style='color:red;'>Crawl4AI completed but returned no content. The page might be empty or inaccessible.</span>"
    except Exception as e:
        return f"❌ <span style='color:red;'>An error occurred while scraping with Crawl4AI: {e}</span>"