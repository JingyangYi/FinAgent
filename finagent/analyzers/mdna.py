from langchain.schema import HumanMessage
from finagent.providers.llm import default_llm

def analyze_mdna(mdna_text: str, prompt_template: str, requirements=None) -> str:
    """
    Analyze Management Discussion & Analysis section using LLM.
    
    Args:
        mdna_text: Text of the MD&A section
        prompt_template: Template for the prompt to send to the LLM
        requirements: Optional specific analysis requirements
    
    Returns:
        Analysis text from the LLM
    """
    if not mdna_text.strip():
        return "No Management Discussion & Analysis data found."
    
    # Prepare the prompt with the MD&A text
    prompt = prompt_template.replace("{{ Insert extracted financial text here }}", mdna_text)
    
    # Add any specific requirements if provided
    if requirements:
        prompt = prompt.replace("{{ Insert user requirements here }}", requirements)
    else:
        prompt = prompt.replace("{{ Insert user requirements here }}", "No additional requirements.")
    
    # Get the analysis from the LLM
    response = default_llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip() 