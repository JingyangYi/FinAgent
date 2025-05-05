from langchain.schema import HumanMessage
from finagent.providers.llm import default_llm
from finagent.extractors.sections import identify_document_type
from typing import Dict

def analyze_title(title_page_text: str, prompt_template: str) -> Dict[str, str]:
    """
    Extract title information from the first page.
    
    Args:
        title_page_text: Text from the first page of the document
        prompt_template: Template for the prompt to send to the LLM
    
    Returns:
        Dictionary with file_title and file_category
    """
    if not title_page_text.strip():
        return {
            "file_title": "unknown-document",
            "file_category": "Unknown"
        }
    
    # Prepare the prompt with the title page text
    prompt = prompt_template.replace("{{ Insert extracted financial text here }}", title_page_text)
    
    # Get the title from the LLM
    response = default_llm.invoke([HumanMessage(content=prompt)])
    title = response.content.strip()
    
    # Determine the category based on the title
    category = identify_document_type(title)
    
    return {
        "file_title": title,
        "file_category": category
    } 