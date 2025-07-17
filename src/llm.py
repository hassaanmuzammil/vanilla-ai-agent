# LLM client configured for the OpenAI API. Compatible with locally hosting LLMs using llama.cpp or Ollama.

from langchain_openai import OpenAI

from src.config import (
    API_KEY,
    BASE_URL,
    MODEL,
)

llm = OpenAI(
    base_url=BASE_URL,
    model=MODEL,
    api_key=API_KEY,
    max_tokens=1024,
    streaming=True,
    verbose=False,
)

if __name__ == "__main__":
    
    # response = llm.invoke("User:Hello, how are you?\nAssistant:")
    # print(response)

    for chunk in llm.stream("User: Tell me a joke.\nAssistant:"):
        print(chunk, end="", flush=True)