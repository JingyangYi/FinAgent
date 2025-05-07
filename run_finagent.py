#!/usr/bin/env python3
"""
Simple wrapper to run the FinAgent package
"""
import sys
import os
from finagent.providers.api_keys import load_api_keys

if __name__ == "__main__":
    # Load API keys from local file
    keys_loaded = load_api_keys()
    if not keys_loaded:
        print("\nPlease fill in your API keys in finagent_keys.json and try again.")
        sys.exit(1)
    
    # Import the financial report generator after API keys are loaded
    from finagent import generate_financial_report
    
    # Get PDF file path from command line argument or prompt
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = input("Enter path to PDF file (press Enter for default sample): ")
        if not pdf_path:
            pdf_path = "files/amazon-10-q-q1-2025.pdf"
            # Check if default file exists
            if not os.path.exists(pdf_path):
                print(f"Default file not found: {pdf_path}")
                pdf_path = input("Please enter a valid PDF file path: ")
                if not pdf_path:
                    print("No valid file path provided. Exiting.")
                    sys.exit(1)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)
    
    # Run the financial analysis
    try:
        result = generate_financial_report(pdf_path)
        print(f"\nAnalysis complete! Report saved to: output/{result['file_title']}.md")
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1) 