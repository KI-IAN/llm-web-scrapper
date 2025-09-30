from langchain_community.document_loaders import FireCrawlLoader
from langchain_core.documents import Document
from config import FIRE_CRAWL_API_KEY


def scrape_with_firecrawl(url: str) -> list[Document]:
    
    loader = FireCrawlLoader(url=url,
                             api_key=FIRE_CRAWL_API_KEY,
                             mode='scrape')
    
    pages = []

    for page in loader.lazy_load():  # type: ignore
        pages.append(page)
        
    return pages

def get_markdown_from_documents(docs: list[Document]) -> str:
    markdown_content = ""
    for i, doc in enumerate(docs):
        markdown_content += f"### Page {i+1}\n"
        markdown_content += f"{doc.page_content}\n\n--------------\n\n"
    return markdown_content


def scrape_and_get_markdown_with_firecrawl(url: str) -> str:
    try:
        docs = scrape_with_firecrawl(url)
        if not docs:
            return "❌ <span style='color:red;'>FireCrawl completed but returned no content. The page might be empty or inaccessible.</span>"
        markdown = get_markdown_from_documents(docs)
        return markdown
    except Exception as e:
        return f"❌ <span style='color:red;'>An error occurred while scraping with FireCrawl: {e}</span>"

   

    