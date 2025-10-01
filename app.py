"""
This module sets up and runs the Gradio web interface for the LLM Web Scraper application.

It orchestrates the UI components, event handling for scraping and LLM extraction,
and integrates with backend services for scraping (FireCrawl, Crawl4AI) and
LLM inference. It also initializes and uses Langfuse for tracing application performance.
"""

import gradio as gr
import firecrawl_client
import crawl4ai_client
import llm_inference_service
from config import LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST
from langfuse import Langfuse, get_client

# Initialize Langfuse if configured
langfuse = None
if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
    Langfuse(
        public_key=LANGFUSE_PUBLIC_KEY, 
        secret_key=LANGFUSE_SECRET_KEY, 
        host=LANGFUSE_HOST
    )
    langfuse = get_client()

def parse_model_provider(selection):
    """
    Parses a model and provider from a selection string.

    The expected format is "<model_name> (<provider>)".

    Args:
        selection (str): The string to parse.

    Returns:
        tuple[str, str]: A tuple containing the model name and provider.

    Raises:
        ValueError: If the selection string is not in the expected format.
    """
    if "(" in selection and ")" in selection:
        model = selection.split(" (")[0].strip()
        provider = selection.split(" (")[1].replace(")", "").strip()
        return model, provider
    raise ValueError(f"Invalid selection format: {selection}")
    
def llm_response_wrapper(query, scrape_result, model_provider_selection, progress=gr.Progress(track_tqdm=True)):
    """
    A generator function that wraps the LLM inference call for the Gradio UI.

    It yields an initial status message, calls the LLM service to extract information,
    and then yields the final result or an error message.

    Args:
        query (str): The user's query for information extraction.
        scrape_result (str): The scraped markdown content from the website.
        model_provider_selection (str): The selected model and provider string.
        progress (gr.Progress, optional): Gradio progress tracker. Defaults to gr.Progress(track_tqdm=True).

    Yields:
        str: Status messages and the final LLM response as a markdown string.
    """
    yield "⏳ Generating response... Please wait."
    
    model, provider = parse_model_provider(model_provider_selection)
    result = llm_inference_service.extract_page_info_by_llm(query, scrape_result, model, provider)
    if not result or (isinstance(result, str) and result.strip() == ""):
        yield "❌ <span style='color:red;'>No information could be extracted from the scraped content. Please check your query or try a different model/provider.</span>"
    yield result

async def scrape_website(url, scraper_selection, progress=gr.Progress(track_tqdm=True)):
    """An async generator that scrapes a website based on user selection for the Gradio UI.

    This function yields an initial status message, then performs the web scraping
    using the selected tool (FireCrawl or Crawl4AI). If Langfuse is configured,
    it wraps the scraping operation in a trace for observability.

    Args:
        url (str): The URL of the website to scrape.
        scraper_selection (str): The scraping tool selected by the user.
        progress (gr.Progress, optional): Gradio progress tracker. Defaults to gr.Progress(track_tqdm=True).

    Yields:
        str: A status message, followed by the scraped markdown content or an error message.
    """
    # 1. First, yield an update to show the loading state and hide the old image.
    yield "⏳ Scraping website... Please wait."

    markdown = ""
    if not langfuse:
        try:
            if scraper_selection == "Scrape with FireCrawl":
                markdown = firecrawl_client.scrape_and_get_markdown_with_firecrawl(url)
            elif scraper_selection == "Scrape with Crawl4AI":
                markdown = await crawl4ai_client.scrape_and_get_markdown_with_crawl4ai(url)
            else:
                markdown = "❌ <span style='color:red;'>Invalid scraper selected.</span>"
        except Exception as e:
            markdown = f"❌ <span style='color:red;'>An unexpected error occurred: {e}</span>"
        yield markdown
        return

    with langfuse.start_as_current_span(name="web-scraping", input={"url": url, "scraper": scraper_selection}) as span:
        try:
            if scraper_selection == "Scrape with FireCrawl":
                markdown = firecrawl_client.scrape_and_get_markdown_with_firecrawl(url)
            elif scraper_selection == "Scrape with Crawl4AI":
                markdown = await crawl4ai_client.scrape_and_get_markdown_with_crawl4ai(url)
            else:
                markdown = "❌ <span style='color:red;'>Invalid scraper selected.</span>"
            span.update_trace(output={"markdown_char_count": len(markdown), "status": "Success"})
        except Exception as e:
            markdown = f"❌ <span style='color:red;'>An unexpected error occurred: {e}</span>"
            span.update_trace(output={"error": str(e), "status": "Error"})
        yield markdown

#Gradio UI
# This block defines the entire Gradio user interface, including layout and component interactions.
with gr.Blocks() as gradio_ui:
    gr.HTML("""
    <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap; margin-bottom: 20px;">
        <h1 style="margin: 0;"> LLM Web Scraper</h1>
        <div style="display: flex; gap: 10px;">
            <a href="https://github.com/langchain-ai/langchain" target="_blank">
                <img src="https://img.shields.io/badge/LangChain-Framework-blue?logo=langchain" alt="LangChain">
            </a>
            <a href="https://ai.google.dev/gemini-api/docs" target="_blank">
                <img src="https://img.shields.io/badge/Gemini%20API-Google-blue?logo=google" alt="Gemini API">
            </a>
            <a href="https://build.nvidia.com/models" target="_blank">
                <img src="https://img.shields.io/badge/NVIDIA%20NIM-API-green?logo=nvidia" alt="NVIDIA NIM">
            </a>
            <a href="https://firecrawl.dev/" target="_blank">
                <img src="https://img.shields.io/badge/FireCrawl-Web%20Scraper-orange?logo=fire" alt="FireCrawl">
            </a>
            <a href="https://docs.crawl4ai.com/" target="_blank">
                <img src="https://img.shields.io/badge/Crawl4AI-Web%20Scraper-blueviolet?logo=github" alt="Crawl4AI">
            </a>

        </div>
    </div>
    """)
    
    gr.HTML("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <span style="font-size: 16px;">📦 <strong>Download the full source code:</strong></span>
        <a href="https://github.com/KI-IAN/llm-web-scrapper" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-View%20Repo-blue?logo=github" alt="GitHub Repo">
        </a>
    </div>
    """)

    gr.HTML("""
    <div style="margin-bottom: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
        <h2 style="margin-top: 0;">How to Use This App</h2>
        <p>This app combines web scraping with the power of Large Language Models (LLMs) to extract specific information from web pages. Here's how it works:</p>
        <ol>
            <li><strong>Enter a URL:</strong> Provide the URL of the web page you want to analyze.</li>
            <li><strong>Define Your Query:</strong> Specify the exact information you're looking for (e.g., product name, price, customer ratings).</li>
            <li><strong>Scrape the Web Page:</strong> Click the "Scrape with FireCrawl" button to extract the content of the page.</li>
            <li><strong>Select Model & Provider:</strong> Choose the LLM model you want to use for information extraction.</li>
            <li><strong>Extract Info by LLM:</strong> Click the "Extract Info by LLM" button to get the information based on your query.</li>
        </ol>
        
        <br />
        <br />
        
        <p><strong>What makes this different from a regular web scraper?</strong>  </p>
    
        <p>Traditional web scrapers require pre-programming to extract product data for each specific website. These scrapers are brittle and can break if the website's design changes. This app uses LLMs to <em>understand</em> your query and extract only the relevant information, saving you time and effort and removing the need for constant maintenance.</p>
    </div>
    """)
    
    
    with gr.Column():
        url_input = gr.Textbox(label="Enter URL to scrape", placeholder="https://example.com/query?search=cat+food", lines=1)
        query_input = gr.Textbox(label="What information do you want to find?", placeholder="Find product name, price, rating etc. / Summarize the content of this page", lines=2)
        
        with gr.Row():
            scraper_dropdown = gr.Dropdown(
                label="Select Scraper",
                choices=["Scrape with Crawl4AI", "Scrape with FireCrawl"],
                value="Scrape with Crawl4AI"
            )
            scrape_btn = gr.Button("Scrape Website")
            clear_btn = gr.Button("Clear")

        scrape_result_textbox = gr.Textbox(label="Scrape Result", lines=20, show_copy_button=True)

        gr.HTML("<hr style='margin-top:10px; margin-bottom:10px;'>")
        gr.Markdown("### 🧠 LLM Extraction")
        gr.Markdown("Use a language model to extract structured information from the scraped content.")
        gr.HTML("<hr style='margin-top:10px; margin-bottom:10px;'>")

    
    with gr.Row():
        
        # Add a single dropdown for model and provider selection
        model_provider_dropdown = gr.Dropdown(
            label="Select Model & Provider",
            choices=[
            "gemini-2.5-flash-lite (google_genai)",
            "gemini-2.5-pro (google_genai)",
            "gemini-2.5-flash (google_genai)",
            "bytedance/seed-oss-36b-instruct (nvidia)",
            "deepseek-ai/deepseek-v3.1 (nvidia)",
            "qwen/qwen3-next-80b-a3b-instruct (nvidia)",
            ],
            value="gemini-2.5-flash-lite (google_genai)"
        )
        
        
        llm_response_btn = gr.Button("Extract Info by LLM")
        cancel_btn = gr.Button("Cancel", variant="stop")
        

    # LLM response output area and loader
    llm_response = gr.Markdown(
        "",
        label="LLM Response",
        show_copy_button=True,
        visible=True
    )
    # Removed custom loader; Gradio will show a spinner automatically during processing.


    scrape_event = scrape_btn.click(
        fn=scrape_website, 
        inputs=[url_input, scraper_dropdown], 
        outputs=[scrape_result_textbox],
    )

    # Clear button functionality
    clear_btn.click(lambda: ("", "", "", ""), outputs=[url_input, query_input, scrape_result_textbox, llm_response])

    llm_event = llm_response_btn.click(
        fn=llm_response_wrapper,
        inputs=[query_input, scrape_result_textbox, model_provider_dropdown],
        outputs=llm_response
    )
    
    cancel_btn.click(fn=lambda: None, inputs=None, outputs=None, cancels=[scrape_event, llm_event])

gradio_ui.launch(server_name="0.0.0.0")
