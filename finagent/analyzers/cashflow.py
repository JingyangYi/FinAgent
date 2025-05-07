from langchain.schema import HumanMessage
from finagent.providers.llm import default_llm

def analyze_cash_flow_statement(cashflow_text: str, prompt_template: str, requirements=None,
                                market_sentiment=None, narrative_themes=None, user_search_results=None) -> str:
    """
    Analyze cash flow statement using LLM.
    
    Args:
        cashflow_text: Text of the cash flow statement section
        prompt_template: Template for the prompt to send to the LLM
        requirements: Optional specific analysis requirements
        market_sentiment: Optional market sentiment from web search
        narrative_themes: Optional narrative themes from web search
        user_search_results: Optional user-specified search results
    
    Returns:
        Analysis text from the LLM
    """
    if not cashflow_text.strip():
        return "No cash flow statement data found."
    
    # Prepare the prompt with the cash flow statement text
    prompt = prompt_template.replace("{{ Insert extracted financial text here }}", cashflow_text)
    
    # Add any specific requirements if provided
    if requirements:
        prompt = prompt.replace("{{ Insert user requirements here }}", requirements)
    else:
        prompt = prompt.replace("{{ Insert user requirements here }}", "No additional requirements.")
    
    # Add web search results if provided
    if market_sentiment:
        prompt = prompt.replace("{{ Insert market sentiment }}", f"**Market Sentiment:**\n{market_sentiment}")
    else:
        prompt = prompt.replace("{{ Insert market sentiment }}", "No market sentiment data available.")
        
    if narrative_themes:
        prompt = prompt.replace("{{ Insert narrative themes }}", f"**Narrative Themes:**\n{narrative_themes}")
    else:
        prompt = prompt.replace("{{ Insert narrative themes }}", "No narrative themes data available.")
    
    if user_search_results:
        prompt = prompt.replace("{{ Insert user search results }}", f"**Custom Search Results:**\n{user_search_results}")
    else:
        prompt = prompt.replace("{{ Insert user search results }}", "")
    
    # Get the analysis from the LLM
    response = default_llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip() 