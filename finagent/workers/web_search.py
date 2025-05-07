"""
Web search module for retrieving financial insights about a company.
Performs web searches to gather market sentiment and narrative themes 
about a company based on its financial filing.
"""

from typing import Dict, Any, Optional, Tuple
from finagent.providers.llm import default_llm
from finagent.providers.tavily import default_search_tool

def web_search(file_title: str, user_search_requirements: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform web search to get financial insights about a company.
    If user_search_requirements is provided, it will perform ONLY the custom search.
    Otherwise, it will perform the default searches (market sentiment and narrative themes).
    
    Args:
        file_title: The file title in format '[company_name_lowercase]-[10q_or_10k]-[fiscal_quarter]-[fiscal_year]'
        user_search_requirements: Optional user-specified search requirements
    
    Returns:
        Dict containing search results
    """
    # Extract company name and time information from file title
    company_name, filing_type, fiscal_quarter, fiscal_year = extract_info_from_title(file_title)
    
    # Use either user-specified search or default searches
    if user_search_requirements:
        # Only perform user-specified search
        return {
            "user_search_results": get_user_specified_search(company_name, filing_type, fiscal_quarter, fiscal_year, user_search_requirements)
        }
    else:
        # Only perform default searches
        return {
            "market_sentiment": get_market_interest(company_name, filing_type, fiscal_quarter, fiscal_year),
            "narrative_themes": get_narrative_themes(company_name, filing_type, fiscal_quarter, fiscal_year)
        }

def extract_info_from_title(file_title: str) -> Tuple[str, str, str, str]:
    """
    Extract company name, filing type, fiscal quarter and year from file title.
    
    Args:
        file_title: The file title in format '[company_name_lowercase]-[10q_or_10k]-[fiscal_quarter]-[fiscal_year]'
        
    Returns:
        Tuple of (company_name, filing_type, fiscal_quarter, fiscal_year)
    """
    parts = file_title.split('-') if file_title else ["unknown"]
    
    company_name = parts[0] if len(parts) > 0 else "unknown"
    filing_type = parts[1] if len(parts) > 1 else "10q"  # Default to 10-Q if not specified
    fiscal_quarter = parts[2] if len(parts) > 2 else "q1"  # Default to Q1 if not specified
    fiscal_year = parts[3] if len(parts) > 3 else "2023"  # Default to current year if not specified
    
    return company_name, filing_type, fiscal_quarter, fiscal_year

def get_market_interest(company_name: str, filing_type: str, fiscal_quarter: str, fiscal_year: str) -> str:
    """
    Get the market's current perception and focus on this stock.
    
    Args:
        company_name: The company name
        filing_type: The filing type (10-K or 10-Q)
        fiscal_quarter: The fiscal quarter
        fiscal_year: The fiscal year
        
    Returns:
        A string containing the market interest analysis
    """
    # Create time-specific search query focusing on market sentiment
    time_specific_query = f"{company_name} stock market sentiment {fiscal_quarter} {fiscal_year} analyst ratings institutional ownership finviz marketbeat tipranks recent"
    
    # Perform the search
    search_results = default_search_tool.invoke(time_specific_query)
    
    # Use the project's default LLM with time-sensitive prompt
    prompt = f"""
    Analyze the following search results about {company_name}'s {fiscal_quarter.upper()} {fiscal_year} financial period.
    Determine the market's perception and focus on this stock for this timeframe.
    
    Focus on:
    1. Recent analyst rating changes or trends
    2. Current institutional ownership and changes
    3. Short interest levels and changes
    4. Overall market sentiment
    
    For each point, include the most recent date available (month/year).
    
    Search results:
    {search_results}
    
    Provide a concise summary of the current market perception in 3-4 bullet points,
    including timeframes for the information when available.
    """
    
    analysis = default_llm.invoke(prompt)
    return analysis.content

def get_narrative_themes(company_name: str, filing_type: str, fiscal_quarter: str, fiscal_year: str) -> str:
    """
    Get themes driving the stock's price or institutional focus.
    
    Args:
        company_name: The company name
        filing_type: The filing type (10-K or 10-Q)
        fiscal_quarter: The fiscal quarter
        fiscal_year: The fiscal year
        
    Returns:
        A string containing the narrative themes analysis
    """
    # Create time-specific query focusing on narrative themes
    time_specific_query = f"{company_name} stock price drivers {fiscal_quarter} {fiscal_year} themes catalyst trends finviz marketbeat zacks nasdaq seekingalpha"
    
    # Perform the search
    search_results = default_search_tool.invoke(time_specific_query)
    
    # Use the project's default LLM with time-sensitive prompt
    prompt = f"""
    Analyze the following search results about {company_name}'s {fiscal_quarter.upper()} {fiscal_year} to identify the key themes
    driving the stock's price or institutional focus during this period.
    
    Focus on:
    1. Key narratives emerging for this specific fiscal period
    2. Growth catalysts being discussed for the near future
    3. Major concerns or risks being highlighted
    4. How this quarter's themes differ from previous periods (if mentioned)
    
    For each theme, include the timeframe it relates to (current quarter, future outlook, etc.).
    
    Search results:
    {search_results}
    
    Provide a concise summary of the key themes driving the stock in 3-4 bullet points,
    including dates or timeframes for each theme when available.
    """
    
    analysis = default_llm.invoke(prompt)
    return analysis.content

def get_user_specified_search(company_name: str, filing_type: str, fiscal_quarter: str, fiscal_year: str, user_requirements: str) -> str:
    """
    Perform a custom web search based on user-specified requirements.
    
    Args:
        company_name: The company name
        filing_type: The filing type (10-K or 10-Q)
        fiscal_quarter: The fiscal quarter
        fiscal_year: The fiscal year
        user_requirements: User-specified search requirements
        
    Returns:
        A string containing the search results analysis
    """
    # Create optimized search query based on user requirements
    refined_query = refine_search_query(company_name, fiscal_quarter, fiscal_year, user_requirements)
    
    # Perform the search
    search_results = default_search_tool.invoke(refined_query)
    
    # Use the project's default LLM to analyze results with time-specific context
    prompt = f"""
    Analyze the following search results about {company_name} for {fiscal_quarter.upper()} {fiscal_year} based on this specific user requirement:
    "{user_requirements}"
    
    Search results:
    {search_results}
    
    Provide a concise and informative analysis that directly addresses the user's requirement.
    Include relevant dates and timeframes when available.
    Format your response as 3-5 bullet points with the most relevant insights.
    """
    
    analysis = default_llm.invoke(prompt)
    return analysis.content

def refine_search_query(company_name: str, fiscal_quarter: str, fiscal_year: str, user_requirements: str) -> str:
    """
    Optimize the user's search requirements into an effective search query.
    
    Args:
        company_name: The company name
        fiscal_quarter: The fiscal quarter
        fiscal_year: The fiscal year
        user_requirements: User-specified search requirements
        
    Returns:
        An optimized search query
    """
    # Use LLM to refine the search query
    prompt = f"""
    I need to perform a web search about the company {company_name} for {fiscal_quarter.upper()} {fiscal_year} based on this request:
    "{user_requirements}"
    
    Please convert this into an effective search query that would yield the most relevant results.
    The query should:
    1. Include the company name
    2. Include the fiscal quarter {fiscal_quarter} and year {fiscal_year}
    3. Use specific financial terminology
    4. Be concise (under 15 words if possible)
    5. Add relevant financial website names like finviz, seekingalpha, marketwatch
    
    Return only the search query string, nothing else.
    """
    
    refined_query = default_llm.invoke(prompt)
    return refined_query.content.strip('"\'')