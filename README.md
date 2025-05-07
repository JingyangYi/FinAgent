# Financial Agent

A modular financial analysis system that extracts and analyzes financial information from 10-K and 10-Q SEC filings.

## API Keys Setup

Before running the application, you need to set up your API keys:

1. Fill in your API keys in the `finagent_keys.json` file in the project directory:
   - `DEEPSEEK_API_KEY` (at least one of DeepSeek or OpenAI is required)
   - `OPENAI_API_KEY` (at least one of DeepSeek or OpenAI is required)
   - `TAVILY_API_KEY` (required for web search functionality)

2. The application will automatically load these keys when it starts.

You can obtain these API keys from:
- DeepSeek: https://platform.deepseek.com/
- OpenAI: https://platform.openai.com/
- Tavily: https://tavily.com/

## Project Structure

The project follows a modular architecture:

```
finagent/            # Package directory
├── models/          # Pydantic data models
├── providers/       # LLM providers and configurations
├── extractors/      # PDF and section extraction logic
├── analyzers/       # Financial analysis components
├── workers/         # Specialized worker modules (web_search.py)
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

# the pdf_file path can be modified in run_finagent.py
```

When prompted, enter the path to a 10-K or 10-Q PDF file. The system will:

1. Extract relevant sections from the filing
2. Ask for any specific analysis requirements
3. Generate an analysis of the Income Statement, Cash Flow Statement, and MD&A
4. Output a markdown report in the `output/` folder


## Provided files

There are a few 10Q files in `files`. Right now the agent does not support 10K files

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