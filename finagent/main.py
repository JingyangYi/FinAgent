import os
import json
from finagent import graph, progress
from finagent.models import FinancialState

def generate_financial_report(pdf_path: str):
    """
    Generate a financial report for the given PDF.
    
    Args:
        pdf_path: Path to the PDF file to analyze
    
    Returns:
        The final state from the graph execution
    """
    # Make output directories
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    os.makedirs("logs", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # # Optional: Log the execution events for debugging
    # stream_events = list(graph.stream({"pdf_path": pdf_path}))
    # with open(f"logs/{base_name}_stream_log.json", "w", encoding="utf-8") as logf:
    #     # Write out the raw AddableUpdatesDicts for inspection
    #     json.dump([dict(e) for e in stream_events], logf, indent=2)
    # progress.close()
    
    # Run the graph to get the final state
    result = graph.invoke({"pdf_path": pdf_path})
    
    # Generate markdown report
    md_report = f"""# Financial Summary: {result['file_title']}

## 🔍 Market Research
"""
    
    # Add web search results based on what's available
    if 'market_sentiment' in result and result['market_sentiment']:
        md_report += f"""### Market Sentiment
{result['market_sentiment']}

"""
    
    if 'narrative_themes' in result and result['narrative_themes']:
        md_report += f"""### Narrative Themes
{result['narrative_themes']}

"""
    
    if 'user_search_results' in result and result['user_search_results']:
        md_report += f"""### Custom Research: {result['user_search_requirements']}
{result['user_search_results']}

"""
    
    # Add financial analysis
    md_report += f"""---

## 📊 Income Statement
{result['analysis_income']}

---

## 💸 Cash Flow Statement
{result['analysis_cashflow']}

---

## 🧠 MD&A Highlights
{result['analysis_mdna']}
"""
    
    # Write the report to a file
    with open(f"output/{result['file_title']}.md", "w", encoding="utf-8") as f:
        f.write(md_report)
    
    # Print a summary
    print(f"\n📁 File Name: {result['file_title']}")
    print("\n📊 Income Statement Analysis:\n", result["analysis_income"])
    print("\n💸 Cash Flow Analysis:\n", result["analysis_cashflow"])
    print("\n🧠 MD&A Highlights:\n", result["analysis_mdna"])
    
    return result

if __name__ == "__main__":
    # Default file path, can be replaced with command line arguments
    pdf_path = input("Enter the path to the PDF file: ")
    if not pdf_path:
        pdf_path = "files/amazon-10-q-q1-2025.pdf"
    
    generate_financial_report(pdf_path) 