from langchain.schema import HumanMessage
from finagent.providers.llm import default_llm

def analyze_income_statement(income_text: str, prompt_template: str, requirements=None) -> str:
    """
    Analyze income statement using LLM.
    
    Args:
        income_text: Text of the income statement section
        prompt_template: Template for the prompt to send to the LLM
        requirements: Optional specific analysis requirements
    
    Returns:
        Analysis text from the LLM
    """
    if not income_text.strip():
        return "No income statement data found."
    
    # Prepare the prompt with the income statement text
    prompt = prompt_template.replace("{{ Insert extracted financial text here }}", income_text)
    
    # Add any specific requirements if provided
    if requirements:
        prompt = prompt.replace("{{ Insert user requirements here }}", requirements)
    else:
        prompt = prompt.replace("{{ Insert user requirements here }}", "No additional requirements.")
    
    # Get the analysis from the LLM
    response = default_llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip() 