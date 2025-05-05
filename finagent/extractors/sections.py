from typing import Dict, List, Any
from finagent.extractors.pdf import find_possible_toc_page, extract_toc_page_numbers
from tqdm import tqdm

def extract_financial_sections(pages: List[str], progress=None) -> Dict[str, Any]:
    """
    Extract key financial sections from PDF pages.
    
    Args:
        pages: List of page texts from the PDF
        progress: Optional tqdm progress bar
    
    Returns:
        Dictionary containing extracted sections
    """
    if progress:
        progress.set_description("🔍 Extracting financial sections")
    
    toc_index = find_possible_toc_page(pages)
    toc_mapping = extract_toc_page_numbers(pages[toc_index]) if toc_index is not None else {}
    
    # Helper function to get section text
    def get_section_text(name):
        indices = toc_mapping.get(name, [])
        return "\n".join(pages[i] for i in indices) if indices else ""
    
    # Extract key sections
    sections = {
        "income_text": get_section_text("income_statement"),
        "cashflow_text": get_section_text("cash_flow_statement"),
        "mdna_text": get_section_text("md_and_a"),
        "title_page_text": pages[0] if pages else ""
    }
    
    if progress:
        progress.update(1)
    
    return sections

def identify_document_type(title_text: str) -> str:
    """
    Identify document type (10-K, 10-Q, etc.) from the title text.
    
    Args:
        title_text: Extracted title text from the document
    
    Returns:
        Document category string
    """
    if "10k" in title_text.lower():
        return "10-K"
    elif "10q" in title_text.lower():
        return "10-Q"
    else:
        return "Unknown" 