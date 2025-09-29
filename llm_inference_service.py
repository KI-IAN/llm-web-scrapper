from langchain.chat_models import init_chat_model


def extract_page_info_by_llm(user_query: str, scraped_markdown_content: str, model_name: str, model_provider: str) -> str:
    
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
    response = llm.invoke(prompt)
    return response.content
    