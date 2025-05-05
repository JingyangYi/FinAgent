# Financial Agent

A modular financial analysis system that extracts and analyzes financial information from 10-K and 10-Q SEC filings.

## Project Structure

The project follows a modular architecture:

```
finagent/            # Package directory
├── models/          # Pydantic data models
├── providers/       # LLM providers and configurations
├── extractors/      # PDF and section extraction logic
├── analyzers/       # Financial analysis components
├── workflows/       # Graph definitions and workflow
├── main.py          # Main entry point
└── README.md        # Package documentation
run_finagent.py      # Main runner script
```

## Installation

### Install dependencies

```bash
# Install dependencies
pip install -r finagent/requirements.txt
```

### Optional: Install package in development mode

```bash
# Install the package in development mode (not required for normal use)
pip install -e .
```

## How to Run

The recommended way to run FinAgent is using the run_finagent.py script in the main directory:

```bash
# Run using the run script (from the main FinAgent directory)
python run_finagent.py

# Or with a specific PDF file
python run_finagent.py files/your-document.pdf
```

When prompted, enter the path to a 10-K or 10-Q PDF file. The system will:

1. Extract relevant sections from the filing
2. Ask for any specific analysis requirements
3. Generate an analysis of the Income Statement, Cash Flow Statement, and MD&A
4. Output a markdown report in the `output/` folder

### Alternative methods (if needed)

You can also run the tool as a Python module (from the main directory):

```bash
python -m finagent
```

Or import the functionality in your own Python code:

```python
from finagent import generate_financial_report

# Generate a financial report
result = generate_financial_report("path/to/your/file.pdf")
```

## Key Components

- **Models**: Define the state model used throughout the workflow
- **Providers**: Configure LLM clients with appropriate settings 
- **Extractors**: Handle PDF text extraction and locate financial sections
- **Analyzers**: Process financial data to generate insights
- **Workflows**: Define the processing graph and execution flow

## Extending the System

To add new functionality:

1. Add new extractors in `extractors/` for different data sources
2. Create new analyzers in `analyzers/` for different types of analysis
3. Update the graph in `workflows/graphs.py` to include new nodes

## Configuration

The system supports multiple LLM providers:
- DeepSeek (default)
- OpenAI

To switch providers, update the `default_llm` in `providers/llm.py`. 