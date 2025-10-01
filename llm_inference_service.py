"""
This module provides the service for interacting with Large Language Models (LLMs).

It is responsible for initializing the Langfuse callback handler for tracing,
constructing the appropriate prompt for information extraction, initializing the
selected chat model, and invoking the model to get a response.
"""

from langchain.chat_models import init_chat_model
from langfuse.langchain import CallbackHandler
from langfuse import Langfuse

from config import LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST

# Initialize Langfuse client
# This block sets up the Langfuse callback handler for LangChain.
# It initializes the Langfuse client and creates a CallbackHandler instance
# only if the required API keys are available. The handler is then added to
# a list of callbacks that can be passed to LLM invocations for tracing.
langfuse_callback_handler = None
callbacks = []

if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
    Langfuse(
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
        host=LANGFUSE_HOST,
    )
    langfuse_callback_handler = CallbackHandler()
    callbacks.append(langfuse_callback_handler)



def extract_page_info_by_llm(user_query: str, scraped_markdown_content: str, model_name: str, model_provider: str) -> str:
    """
    Extracts information from scraped content using a specified Large Language Model.

    This function constructs a detailed prompt, initializes the selected chat model,
    and invokes it with the scraped content and user query. If Langfuse is configured,
    it uses a callback handler to trace the LLM interaction.

    Args:
        user_query (str): The user's query specifying what information to extract.
        scraped_markdown_content (str): The markdown content from the scraped web page.
        model_name (str): The name of the LLM to use for extraction.
        model_provider (str): The provider of the LLM (e.g., 'google_genai', 'nvidia').

    Returns:
        str: The content of the LLM's response.
    """
    
    if not scraped_markdown_content:
        return "No relevant information found to answer your question."

    context = scraped_markdown_content
    
    prompt = f""" 
    You are an expert assistant who can extract useful information from the content provided to you. Most of the time, 
    the content will be product pages from e-commerce websites. Users will ask you to extract product information such as product name, price, rating, etc.

    Please provide your identity (model name and provider if applicable) at the beginning of your answer.

    Use the following context to answer the user's question. Provide the final answer in a markdown table format if you are asked to extract product information. 
    If you can't extract anything useful provide in plain markdown format.
    
    If user asks for JSON format, please provide the answer in JSON format only.
    
    User will mostly request you to extract product information but can also ask you to extract other information from the content. 
    So always read the user query carefully and extract information accordingly.
    
    If you do not find or know the answer, do not hallucinate, do not try to generate fake answers.
    If no Context is given, simply state "No relevant information found to answer your question."
    
    Context: 
    {context}

    Question:
    {user_query}
    
    Your Identity:
    
    Answer:
    
    """
    
    llm = init_chat_model(model_name, model_provider=model_provider)
    response = llm.invoke(prompt, config={"callbacks": callbacks})
    return response.content
    