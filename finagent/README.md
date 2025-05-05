# Financial Agent

A modular financial analysis system that extracts and analyzes financial information from 10-K and 10-Q SEC filings.

## Project Structure

The project follows a modular architecture:

```
finagent/
├── models/          # Pydantic data models
├── providers/       # LLM providers and configurations
├── extractors/      # PDF and section extraction logic
├── analyzers/       # Financial analysis components
├── workflows/       # Graph definitions and workflow
├── main.py          # Main entry point
└── README.md        # This file
```

## Installation

### Install from local directory

```bash
# Clone the repository
git clone https://your-repository-url.git
cd your-repository-dir

# Install the package in development mode
pip install -e .
```

### Install dependencies only

```bash
# Install dependencies
pip install -r finagent/requirements.txt
```

## How to Run

### As a module

```bash
# Run directly as a Python module
python -m finagent [path/to/your/file.pdf]
```

### From Python code

```python
from finagent import generate_financial_report

# Generate a financial report
result = generate_financial_report("path/to/your/file.pdf")
```

### Using the run script

```bash
# Run using the run script
python finagent/run.py [path/to/your/file.pdf]
```

When prompted, enter the path to a 10-K or 10-Q PDF file. The system will:

1. Extract relevant sections from the filing
2. Ask for any specific analysis requirements
3. Generate an analysis of the Income Statement, Cash Flow Statement, and MD&A
4. Output a markdown report in the `output/` folder

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