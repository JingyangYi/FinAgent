"""
Tavily search provider module.
"""

import os
from langchain_tavily.tavily_search import TavilySearch
from finagent.providers.api_keys import get_api_key

def get_tavily_search(max_results=3):
    """
    Initialize and return a Tavily search tool.
    Uses API key stored in the local file.
    
    Args:
        max_results: Maximum number of search results to return
        
    Returns:
        An initialized TavilySearch tool
    """
    api_key = get_api_key("TAVILY_API_KEY")
    if api_key:
        os.environ["TAVILY_API_KEY"] = api_key
    
    return TavilySearch(
        max_results=max_results,
        search_depth="basic",
        topic="finance"  # Using finance since this is a financial application
    )

# Default search tool that can be imported directly
try:
    default_search_tool = get_tavily_search()
except:
    print("WARNING: Failed to initialize Tavily search tool. Make sure API key is set in ~/.finagent_keys.json") 