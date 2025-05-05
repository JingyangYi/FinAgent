from setuptools import setup, find_packages

setup(
    name="finagent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pdfplumber>=0.5.28",
        "langgraph>=0.0.15",
        "langchain>=0.1.0",
        "langchain-core>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-community>=0.0.5",
        "langchain-deepseek>=0.0.1",
        "pydantic>=2.5.0",
        "tqdm>=4.66.0",
    ],
    author="FinAgent Team",
    description="A modular financial analysis system for SEC filings",
    keywords="finance, analysis, sec, 10-k, 10-q, llm",
    python_requires=">=3.8",
) 