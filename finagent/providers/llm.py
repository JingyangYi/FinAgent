import os
import getpass
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from finagent.providers.api_keys import get_api_key
from langchain.schema import HumanMessage

# Define a fallback LLM that returns error messages instead of crashing
class FallbackLLM:
    """
    A fallback LLM that returns error messages when no real LLM is available.
    """
    def __init__(self, error_message="API key missing. Please add your API keys to finagent_keys.json"):
        self.error_message = error_message
        
    def invoke(self, messages):
        """
        Return an error message instead of actually invoking an LLM.
        """
        if isinstance(messages, str):
            return self.error_message
        else:
            class DummyResponse:
                def __init__(self, content):
                    self.content = content
            return DummyResponse(self.error_message)

def get_deepseek_llm(temperature=0, max_tokens=None, timeout=None, max_retries=2):
    """
    Initialize and return a DeepSeek chat model.
    """
    api_key = get_api_key("DEEPSEEK_API_KEY")
    if api_key:
        os.environ["DEEPSEEK_API_KEY"] = api_key
    
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
    api_key = get_api_key("OPENAI_API_KEY")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    return ChatOpenAI(
        model=model,
        temperature=temperature
    )

def get_llm(provider="deepseek", **kwargs):
    """
    Factory function to get an LLM based on specified provider.
    """
    # Try to use the specified provider first
    if provider.lower() == "deepseek" and get_api_key("DEEPSEEK_API_KEY"):
        return get_deepseek_llm(**kwargs)
    elif provider.lower() == "openai" and get_api_key("OPENAI_API_KEY"):
        return get_openai_llm(**kwargs)
    
    # If the specified provider's API key is missing, try to use the alternative
    if provider.lower() == "deepseek" and get_api_key("OPENAI_API_KEY"):
        print("DeepSeek API key not found. Using OpenAI instead.")
        return get_openai_llm(**kwargs)
    elif provider.lower() == "openai" and get_api_key("DEEPSEEK_API_KEY"):
        print("OpenAI API key not found. Using DeepSeek instead.")
        return get_deepseek_llm(**kwargs)
    
    # If neither key is available, use the fallback
    print("No valid API key found. Using fallback LLM.")
    return FallbackLLM()

# Default LLM that can be imported directly
# Try DeepSeek first, fall back to OpenAI if necessary
try:
    default_llm = get_deepseek_llm()
except Exception as e:
    try:
        default_llm = get_openai_llm()
    except Exception as e:
        print(f"WARNING: Failed to initialize default LLM. Make sure API keys are set in finagent_keys.json")
        # Always assign a value to default_llm, even if it's just a fallback
        default_llm = FallbackLLM() 