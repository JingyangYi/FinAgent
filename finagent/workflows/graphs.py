from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from finagent.models.state import FinancialState
from finagent.workflows.nodes import (
    extract_title_node,
    extract_10k_sections_node,
    extract_10q_sections_node,
    get_analysis_requirements_node,
    analyze_sections_node,
    route_by_category,
    progress
)

def create_financial_analysis_graph():
    """
    Creates the main financial analysis workflow graph.
    
    Returns:
        The compiled workflow graph
    """
    # Create state graph
    workflow = StateGraph(state_schema=FinancialState)
    
    # Add nodes
    workflow.add_node("extract_title", RunnableLambda(extract_title_node))
    workflow.add_node("extract_10_K", RunnableLambda(extract_10k_sections_node))
    workflow.add_node("extract_10_Q", RunnableLambda(extract_10q_sections_node))
    workflow.add_node("get_analysis_requirements", RunnableLambda(get_analysis_requirements_node))
    workflow.add_node("analyze_sections", RunnableLambda(analyze_sections_node))
    
    # Set up the workflow
    workflow.set_entry_point("extract_title")
    
    # Add conditional routing based on file category
    workflow.add_conditional_edges(
        "extract_title",
        route_by_category,
        {
            "10-K": "extract_10_K",
            "10-Q": "extract_10_Q",
            "Unknown": "extract_10_Q", 
        }
    )
    
    # Continue with the rest of the workflow
    workflow.add_edge("extract_10_K", "get_analysis_requirements")
    workflow.add_edge("extract_10_Q", "get_analysis_requirements")
    workflow.add_edge("get_analysis_requirements", "analyze_sections")
    workflow.set_finish_point("analyze_sections")
    
    # Compile the graph
    return workflow.compile()

# Create the main graph
graph = create_financial_analysis_graph() 