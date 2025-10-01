import asyncio
from crawl4ai import AsyncWebCrawler


async def scrape_and_get_markdown_with_crawl4ai(url: str) -> str:
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url) 

            markdown_content = "❌ <span style='color:red;'>Crawl4AI completed but returned no content. The page might be empty or inaccessible.</span>"

            if result and result.markdown:
                markdown_content = result.markdown
            
            return markdown_content
    except Exception as e:
        return f"❌ <span style='color:red;'>An error occurred while scraping with Crawl4AI: {e}</span>"