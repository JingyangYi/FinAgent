import os
import getpass
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek

def get_deepseek_llm(temperature=0, max_tokens=None, timeout=None, max_retries=2):
    """
    Initialize and return a DeepSeek chat model.
    """
    if not os.getenv("DEEPSEEK_API_KEY"):
        os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter DeepSeek API Key: ")
    
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        max_retries=max_retries,
    )

def get_openai_llm(model="gpt-4o", temperature=0):
    """
    Initialize and return an OpenAI chat model.
    """
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter OpenAI API Key: ")
    
    return ChatOpenAI(
        model=model,
        temperature=temperature
    )

def get_llm(provider="deepseek", **kwargs):
    """
    Factory function to get an LLM based on specified provider.
    """
    if provider.lower() == "deepseek":
        return get_deepseek_llm(**kwargs)
    elif provider.lower() == "openai":
        return get_openai_llm(**kwargs)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

# Default LLM that can be imported directly
default_llm = get_deepseek_llm() 