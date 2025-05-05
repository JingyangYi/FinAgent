import pdfplumber
import re
import os
import contextlib
from typing import List, Optional, Dict

def extract_text(file_path: str) -> List[str]:
    """
    Extracts all text from the specified PDF and returns it as a list of page texts.
    """
    pages = []
    # suppress CropBox warnings from pdfplumber/pdfminer
    with open(os.devnull, 'w') as devnull, contextlib.redirect_stderr(devnull):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
    return pages

def find_possible_toc_page(pages: List[str], max_pages: int = 5) -> Optional[int]:
    """
    Returns the index of the page most likely to contain the table of contents.
    Looks for multiple 'Item X' entries.
    Only looks for the first 5 pages.
    """
    # edit_1: broaden regex to match Item1, item1, Item.1, item-1, etc.
    item_pattern = re.compile(r'\bitem\W{0,3}(\d+[A]?)', re.IGNORECASE)
    
    if len(pages) > max_pages:
        pages = pages[:max_pages]
    for i, page in enumerate(pages):
        # Heuristic: if at least 2 item entries are found on a page, it's likely TOC
        items_found = item_pattern.findall(page)
        if len(set(items_found)) >= 2:
            return i
    print("No TOC found")
    return None

def extract_toc_page_numbers(toc_text: str) -> Dict[str, List[int]]:
    """
    Given the text of a TOC page, returns a dict of the last-seen page numbers for:
      - income_statement
      - cash_flow_statement
      - md_and_a
      - market_risk
    Falls back to broad keyword matching if the specific patterns miss.
    """
    # 1) Primary, specific patterns
    primary_patterns = {
        'income_statement': re.compile(
            r'(?:Consolidated\s+)?(?:Income Statement|Statements?\s+of\s+(?:Income|Operations|Comprehensive Income))',
            re.IGNORECASE
        ),
        'cash_flow_statement': re.compile(
            r'(?:Consolidated\s+)?(?:Cash Flow Statement|Statements?\s+of\s+Cash Flows)',
            re.IGNORECASE
        ),
        'md_and_a': re.compile(
            r'(?:Management[’\']s Discussion and Analysis|Management Discussion\s*&\s*Analysis|MD&A)',
            re.IGNORECASE
        ),
        'market_risk': re.compile(
            r'(?:Quantitative and Qualitative Disclosures About Market Risk|Disclosures About Market Risk)',
            re.IGNORECASE
        ),
    }

    # 2) Fallback, broad keyword patterns
    fallback_patterns = {
        'income_statement': re.compile(r'\bincome\b', re.IGNORECASE),
        'cash_flow_statement': re.compile(r'\bcash flows?\b', re.IGNORECASE),
        'md_and_a': re.compile(r'\bMD&A\b', re.IGNORECASE),
        'market_risk': re.compile(r'\brisks?\b', re.IGNORECASE),
    }

    results = {key: [] for key in primary_patterns}
    
    # Extract all page numbers and their associated line text from TOC
    all_toc_entries = []
    for line in toc_text.splitlines():
        page_num = re.search(r'(\d+)\s*$', line)
        if page_num:
            all_toc_entries.append((int(page_num.group(1)), line))
    
    # Sort by page number
    all_toc_entries.sort(key=lambda x: x[0])
    
    # Find the starting pages for our items of interest
    items_of_interest = {}
    for page, line in all_toc_entries:
        for key, pattern in primary_patterns.items():
            if pattern.search(line):
                if key not in items_of_interest:
                    items_of_interest[key] = []
                items_of_interest[key].append(page)
    
    # Fallback for items not found
    for page, line in all_toc_entries:
        for key, pattern in fallback_patterns.items():
            if key not in items_of_interest and pattern.search(line):
                if key not in items_of_interest:
                    items_of_interest[key] = []
                items_of_interest[key].append(page)
    
    # Calculate page ranges for each item
    for key, start_pages in items_of_interest.items():
        for start_page in start_pages:
            # Find the next page number in the TOC after this one
            next_pages = [p for p, _ in all_toc_entries if p > start_page]
            if next_pages:
                next_page = min(next_pages)
                # Add all pages from start_page to next_page-1
                results[key].extend(range(start_page, next_page))
            else:
                # If this is the last entry, just add this page
                results[key].append(start_page)

    # page numbers are 1-indexed
    for key in results:
        results[key] = [p - 1 for p in results[key]]

    return results
