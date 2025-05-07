"""
FinAgent - A modular financial analysis system for SEC filings
"""
# The API keys will be loaded when importing any provider
from finagent.workflows.graphs import graph, progress
from finagent.models.state import FinancialState
from finagent.main import generate_financial_report

__version__ = '0.1.0'

__all__ = [
    'graph',
    'progress',
    'FinancialState',
    'generate_financial_report'
] 