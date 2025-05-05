from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FinancialState(BaseModel):
    # Required on entry
    pdf_path: str
    pdf_pages: List[str] = []

    # Filled out by extract_pdf_sections
    income_text: Optional[str] = None
    cashflow_text: Optional[str] = None
    mdna_text: Optional[str] = None

    # Filled out by analyze_sections
    analysis_income: Optional[str] = None
    analysis_cashflow: Optional[str] = None
    analysis_mdna: Optional[str] = None
    
    # User requirements for analysis
    income_requirements: Optional[str] = None
    cashflow_requirements: Optional[str] = None
    mdna_requirements: Optional[str] = None

    # Filled out by extract_title
    file_title: Optional[str] = None
    file_category: Optional[str] = None 