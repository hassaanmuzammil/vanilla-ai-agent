# LLM client configured for the OpenAI API. Compatible with locally hosting LLMs using llama.cpp or Ollama.

from langchain_openai import OpenAI

from config import (
    API_KEY,
    BASE_URL,
    MODEL,
)

llm = OpenAI(
    base_url=BASE_URL,
    model=MODEL,
    api_key=API_KEY,
    max_tokens=1000,
    streaming=True,
    verbose=False,
)