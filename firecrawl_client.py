"""
This module provides a client for interacting with the FireCrawl service.

It encapsulates the logic for scraping a website using the FireCrawlLoader from
LangChain, converting the scraped documents into a single markdown string, and
handling potential errors during the process.
"""

from langchain_community.document_loaders import FireCrawlLoader
from langchain_core.documents import Document
from config import FIRE_CRAWL_API_KEY


def scrape_with_firecrawl(url: str) -> list[Document]:
    """
    Scrapes a given URL using FireCrawl and returns the content as a list of Documents.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        list[Document]: A list of LangChain Document objects, where each document
                        represents a scraped page.
    """
    loader = FireCrawlLoader(url=url,
                             api_key=FIRE_CRAWL_API_KEY,
                             mode='scrape')
    
    pages = []

    for page in loader.lazy_load():  # type: ignore
        pages.append(page)
        
    return pages

def get_markdown_from_documents(docs: list[Document]) -> str:
    """
    Converts a list of LangChain Documents into a single markdown string.

    Each document's content is appended, separated by a horizontal rule.

    Args:
        docs (list[Document]): A list of Document objects to process.

    Returns:
        str: A string containing the combined content in markdown format.
    """
    markdown_content = ""
    for i, doc in enumerate(docs):
        markdown_content += f"### Page {i+1}\n"
        markdown_content += f"{doc.page_content}\n\n--------------\n\n"
    return markdown_content


def scrape_and_get_markdown_with_firecrawl(url: str) -> str:
    """
    Orchestrates the scraping of a URL with FireCrawl and returns the content as markdown.

    This is the main entry point function for this module. It handles the full
    process of scraping, content conversion, and error handling.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The scraped content in markdown format, or a formatted error message string if an issue occurs.
    """
    try:
        docs = scrape_with_firecrawl(url)
        if not docs:
            return "❌ <span style='color:red;'>FireCrawl completed but returned no content. The page might be empty or inaccessible.</span>"
        markdown = get_markdown_from_documents(docs)
        return markdown
    except Exception as e:
        return f"❌ <span style='color:red;'>An error occurred while scraping with FireCrawl: {e}</span>"

   

    