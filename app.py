import gradio as gr

import firecrawl_client
import llm_inference_service

def parse_model_provider(selection):
    # Expected format: "<model_name> (<provider>)"
    if "(" in selection and ")" in selection:
        model = selection.split(" (")[0].strip()
        provider = selection.split(" (")[1].replace(")", "").strip()
        return model, provider
    raise ValueError(f"Invalid selection format: {selection}")
    
def llm_response_wrapper(query, scrape_result, model_provider_selection):
    model, provider = parse_model_provider(model_provider_selection)
    result = llm_inference_service.extract_page_info_by_llm(query, scrape_result, model, provider)
    if not result or (isinstance(result, str) and result.strip() == ""):
        return "❌ <span style='color:red;'>No information could be extracted from the scraped content. Please check your query or try a different model/provider.</span>"
    return result

#Gradio UI
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
            <a href="https://github.com/crawl4ai/crawl4ai" target="_blank">
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

    
    with gr.Column():
        url_input = gr.Textbox(label="Enter URL to scrape", placeholder="https://example.com/query?search=cat+food", lines=1)
        # search_query_input = gr.Textbox(label="Enter your query", placeholder="Paw paw fish adult cat food", lines=1)
        query_input = gr.Textbox(label="What information do you want to find?", placeholder="Find product name, price, rating", lines=1)
        scrape_btn = gr.Button("Scrape with FireCrawl")
        
        scrape_result_textbox = gr.Textbox(label="Scrape Result", lines=20, show_copy_button=True)
        
        label_llm_section = gr.Label("Use LLM to extract information from the scraped content")
        gr.HTML("<hr>")
        
    
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
        
        
        llm_response_btn = gr.Button("Extracted Info by LLM")
        

    # LLM response output area and loader
    llm_response = gr.Markdown(
        "\n" * 9,  # 9 newlines + 1 line for empty content = 10 lines minimum
        label="LLM Response",
        show_copy_button=True,
        visible=True
    )
    # Removed custom loader; Gradio will show a spinner automatically during processing.


    scrape_btn.click(fn=firecrawl_client.scrape_and_get_markdown_with_firecrawl, inputs=url_input, outputs=scrape_result_textbox)

    llm_response_btn.click(
        fn=llm_response_wrapper,
        inputs=[query_input, scrape_result_textbox, model_provider_dropdown],
        outputs=llm_response
    )

gradio_ui.launch(server_name="0.0.0.0")
