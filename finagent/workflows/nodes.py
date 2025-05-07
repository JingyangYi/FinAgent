from typing import Dict, Any
from tqdm import tqdm
from finagent.models.state import FinancialState
from finagent.extractors.pdf import extract_text
from finagent.extractors.sections import extract_financial_sections, identify_document_type
from finagent.analyzers.income import analyze_income_statement
from finagent.analyzers.cashflow import analyze_cash_flow_statement
from finagent.analyzers.mdna import analyze_mdna
from finagent.analyzers.title import analyze_title
from finagent.workers.web_search import web_search
from finagent.workflows.config import (
    prompt_template_analyze_income_statement,
    prompt_template_analyze_cash_flow_statement,
    prompt_template_analyze_md_and_a,
    prompt_template_analyze_file_title,
)

progress = tqdm(total=6, bar_format="{desc:<50}{percentage:3.0f}%|{bar:30}| {n_fmt}/{total_fmt}")

def extract_title_node(state: FinancialState) -> Dict[str, Any]:
    """
    Node for extracting the file title from the first page.
    """
    progress.set_description("📄 Step 1: Extracting file name")
    
    # Extract PDF pages if not already extracted
    pages = state.pdf_pages
    if not pages:
        pages = extract_text(state.pdf_path)
    
    # Get the title page text and analyze it
    title_page_text = pages[0] if pages else ""
    title_info = analyze_title(title_page_text, prompt_template_analyze_file_title)
    
    progress.update(1)
    
    return {
        "file_title": title_info["file_title"],
        "file_category": title_info["file_category"],
        "pdf_pages": pages if not state.pdf_pages else state.pdf_pages
    }

def get_search_requirements_node(state: FinancialState) -> Dict[str, Any]:
    """
    Node for getting user-specified search requirements before web search.
    """
    print("\n" + "="*50)
    print("Before web search:")
    print("Do you have any specific topics you'd like to research about this company?")
    print("For example: 'Recent lawsuits', 'Planned acquisitions', 'CEO changes', etc.")
    print("NOTE: If you provide a custom topic, ONLY that topic will be searched.")
    print("If you leave this blank, the system will search for market sentiment and narrative themes.")
    print("="*50 + "\n")
    
    search_input = input("Your search requirements (press Enter to use default searches): ").strip()
    
    return {
        "user_search_requirements": search_input if search_input else None
    }

def web_search_node(state: FinancialState) -> Dict[str, Any]:
    """
    Node for web search:
    - If user provided search requirements: performs custom search
    - If no requirements: performs default searches for market sentiment and narrative themes
    """
    if state.user_search_requirements:
        progress.set_description("🔍 Step 2: Web Search for User-Specified Topics")
    else:
        progress.set_description("🔍 Step 2: Web Search for Market Sentiments and Themes")
    
    # Pass user search requirements to web_search function
    search_results = web_search(state.file_title, state.user_search_requirements)
    
    # Update progress after web search is complete
    progress.update(1)
    
    # Simply return all search results (either user search or default searches)
    return search_results

def extract_10k_sections_node(state: FinancialState) -> Dict[str, Any]:
    """
    Node for extracting sections from 10-K reports.
    """
    progress.set_description("🔍 Step 3: Extracting 10-K PDF sections")
    sections = extract_financial_sections(state.pdf_pages, progress)
    return sections

def extract_10q_sections_node(state: FinancialState) -> Dict[str, Any]:
    """
    Node for extracting sections from 10-Q reports.
    """
    progress.set_description("🔍 Step 3: Extracting 10-Q PDF sections")
    sections = extract_financial_sections(state.pdf_pages, progress)
    return sections

def get_analysis_requirements_node(state: FinancialState) -> Dict[str, Any]:
    """
    Node for getting user-specified analysis requirements.
    """
    print("\n" + "="*50)
    print("Before analyzing the Financial Statements:")
    print("Do you have any specific requirements or focus areas for the analysis?")
    print("For example: 'Focus on profitability trends' or 'Analyze future growth prospects'")
    print("="*50)
    
    print("\nIncome Statement Analysis Requirements:")
    income_input = input("Your requirements (press Enter to skip): ").strip()
    
    print("\nCash Flow Statement Analysis Requirements:")
    cashflow_input = input("Your requirements (press Enter to skip): ").strip()
    
    print("\nManagement Discussion & Analysis Requirements:")
    mdna_input = input("Your requirements (press Enter to skip): ").strip()
    
    return {
        "income_requirements": income_input if income_input else None,
        "cashflow_requirements": cashflow_input if cashflow_input else None,
        "mdna_requirements": mdna_input if mdna_input else None
    }

def analyze_sections_node(state: FinancialState) -> Dict[str, Any]:
    """
    Node for analyzing all financial sections.
    """
    # Prepare web search data
    market_sentiment = state.market_sentiment if hasattr(state, 'market_sentiment') else None
    narrative_themes = state.narrative_themes if hasattr(state, 'narrative_themes') else None
    user_search_results = state.user_search_results if hasattr(state, 'user_search_results') else None
    
    # Analyze Income Statement
    progress.set_description("📊 Step 4: Analyzing Income Statement")
    analysis_income = analyze_income_statement(
        state.income_text, 
        prompt_template_analyze_income_statement, 
        state.income_requirements,
        market_sentiment,
        narrative_themes,
        user_search_results
    )
    progress.update(1)

    # Analyze Cash Flow Statement
    progress.set_description("📊 Step 5: Analyzing Cash Flow Statement")
    analysis_cashflow = analyze_cash_flow_statement(
        state.cashflow_text, 
        prompt_template_analyze_cash_flow_statement, 
        state.cashflow_requirements,
        market_sentiment,
        narrative_themes,
        user_search_results
    )
    progress.update(1)

    # Analyze MD&A
    progress.set_description("📊 Step 6: Analyzing MD&A")
    analysis_mdna = analyze_mdna(
        state.mdna_text, 
        prompt_template_analyze_md_and_a, 
        state.mdna_requirements,
        market_sentiment,
        narrative_themes,
        user_search_results
    )
    progress.update(1)
    
    return {
        "analysis_income": analysis_income,
        "analysis_cashflow": analysis_cashflow,
        "analysis_mdna": analysis_mdna
    }

# Router function to determine which extraction method to use
def route_by_category(state: FinancialState) -> str:
    """
    Router function to determine which extraction method to use.
    """
    return state.file_category 