---
title: LLM Web Scraper
emoji: 🕸️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# LLM Web Scraper (🕸️ → 🤖 → 🧠 → ❓ → 📄)

Scrape any web page, ask questions, and get structured answers powered by LangChain, FireCrawl/Crawl4AI and leading LLMs from NVIDIA and Google—all wrapped in a clean Gradio interface.

🔗 **Live Demo**: https://huggingface.co/spaces/frkhan/llm-web-scrapper

🔗 **Read Full Story**: [From Broken Selectors to Intelligent Scraping: A Journey into LLM-Powered Web Automation](https://medium.com/@frkhan/from-broken-selectors-to-intelligent-scraping-a-journey-into-llm-powered-web-automation-fc76d5fe2dbc)

---

### 🚀 Features

-   🕸️ **Multi-Backend Scraping**: Choose between `FireCrawl` for robust, API-driven scraping and `Crawl4AI` for local, Playwright-based scraping.
-   🧠 **Intelligent Extraction**: Use powerful LLMs (NVIDIA or Google Gemini) to understand your query and extract specific information from scraped content.
-   📊 **Structured Output**: Get answers in markdown tables, JSON, or plain text, as requested.
-   📈 **Full Observability**: Integrated with `Langfuse` to trace both scraping and LLM-extraction steps.
-   ✨ **Interactive UI**: A clean and simple interface built with `Gradio`.
-   🐳 **Docker-Ready**: Comes with `Dockerfile` and `docker-compose` configurations for easy local and production deployment.

---

### 🛠️ Tech Stack

| Component | Purpose |
| :--- | :--- |
| **LangChain** | Orchestration of LLM calls |
| **FireCrawl / Crawl4AI** | Web scraping backends |
| **NVIDIA / Gemini** | LLM APIs for information extraction |
| **Langfuse** | Tracing and observability for all operations |
| **Gradio** | Interactive web UI |
| **Docker** | Containerized deployment |
| **Playwright**| Web scraping using Crawl4AI|

---

## 📦 Installation

### Option 1: Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KI-IAN/llm-web-scrapper.git
    cd llm-web-scrapper
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers (for Crawl4AI):**
    ```bash
    playwright install
    ```

4.  **Create a `.env` file** in the root directory with your API keys:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    NVIDIA_API_KEY=your_nvidia_api_key
    FIRECRAWL_API_KEY=your_firecrawl_api_key
    
    # Optional: For Langfuse tracing
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_SECRET_KEY=sk-lf-...
    LANGFUSE_HOST=https://cloud.langfuse.com
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```

---

### Option 2: Run with Docker

1.  **For Production:**
    This uses the standard `docker-compose.yml`.
    ```bash
    docker compose up --build
    ```

2.  **For Local Development (with live code reload):**
    This uses `docker-compose.dev.yml` to mount your local code into the container.
    ```bash
    docker compose -f docker-compose.dev.yml up --build
    ```

Access the app at http://localhost:12200.

---

## 🔑 Getting API Keys

To use this app, you'll need API keys for **Google Gemini**, **NVIDIA NIM**, and **FireCrawl**. For full observability, you'll also need keys for **Langfuse**.

### 🌐 Gemini API Key
Gemini is Google's family of generative AI models. To get an API key:

1. Visit the [Google AI Studio](https://aistudio.google.com/api-keys).
2. Sign in with your Google account.
3. Click **"Create API Key"** and copy the key shown.
4. Use this key in your `.env` file or configuration as `GEMINI_API_KEY`.

> Note: Gemini API access may be limited based on region or account eligibility. Check the Gemini API [Rate Limits here](https://ai.google.dev/gemini-api/docs/rate-limits)

### 🌐 NVIDIA NIM API Key
NIM (NVIDIA Inference Microservices) provides hosted models via REST APIs. To get started:

1. Go to the [NVIDIA API Catalog](https://build.nvidia.com/?integrate_nim=true&hosted_api=true&modal=integrate-nim).
2. Choose a model (e.g., `nim-gemma`, `nim-mistral`, etc.) and click **"Get API Key"**.
3. Sign in or create an NVIDIA account if prompted.
4. Copy your key and use it as `NVIDIA_NIM_API_KEY` in your environment.

> Tip: You can test NIM endpoints directly in the browser before integrating.

### 🌐 FireCrawl API Key

1.  Sign up at [FireCrawl](https://www.firecrawl.dev/).
2.  Find your API key in the dashboard.

### 🌐 Langfuse API Keys (Optional)

1.  Sign up or log in at [Langfuse Cloud](https://cloud.langfuse.com/).
2.  Navigate to your project settings and then to the "API Keys" tab.
3.  Create a new key pair to get your `LANGFUSE_PUBLIC_KEY` (starts with `pk-lf-...`) and `LANGFUSE_SECRET_KEY` (starts with `sk-lf-...`).
4.  Add these to your `.env` file to enable tracing.

---

## 🧪 How to Use

1.  **Enter a URL**: Provide the URL of the web page you want to analyze.
2.  **Define Your Query**: Specify what you want to extract (e.g., "product name, price, and rating" or "summarize this article").
3.  **Scrape the Web Page**: Choose a scraper (`Crawl4AI` or `FireCrawl`) and click **"Scrape Website"**.
4.  **Select Model & Provider**: Choose an LLM to process the scraped content.
5.  **Extract Info**: Click **"Extract Info by LLM"** to get a structured answer.

---

### 📁 File Structure

```
llm-web-scrapper/
├── .env                  # Local environment variables (not tracked by git)
├── .github/              # GitHub Actions workflows
├── .gitignore
├── docker-compose.yml    # Production Docker configuration
├── docker-compose.dev.yml# Development Docker configuration
├── Dockerfile
├── requirements.txt
├── app.py                # Gradio UI and application logic
├── config.py             # Environment variable loading
├── crawl4ai_client.py    # Client for Crawl4AI scraper
├── firecrawl_client.py   # Client for FireCrawl scraper
└── llm_inference_service.py # Logic for LLM calls
```

---

## 📜 License

This project is open-source and distributed under the **MIT License**. Feel free to use, modify, and distribute it.

---

## 🤝 Acknowledgements

-   [LangChain](https://www.langchain.com/) for orchestrating LLM interactions.
-   [FireCrawl](https://www.firecrawl.dev/) & [Crawl4AI](https://docs.crawl4ai.com/) for providing powerful scraping backends.
-   [NVIDIA AI Endpoints](https://build.nvidia.com/models) & [Google Gemini API](https://ai.google.dev/gemini-api/docs) for their state-of-the-art LLMs.
-   [Langfuse](https://langfuse.com/) for providing excellent observability tools.
-   [Gradio](https://www.gradio.app/) for making UI creation simple and elegant.
-   [Docker](https://www.docker.com/) for containerization
-   [Playwright](https://playwright.dev/) for web scraping using [Crawl4AI](https://docs.crawl4ai.com/)

---
