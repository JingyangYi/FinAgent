#!/usr/bin/env python3
"""
Simple wrapper to run the FinAgent package
"""
import sys
from finagent import generate_financial_report

if __name__ == "__main__":
    # Get PDF file path from command line argument or prompt
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # pdf_path = input("Enter path to PDF file: ")
        pdf_path = "files/amazon-10-q-q1-2025.pdf"
    # Run the financial analysis
    result = generate_financial_report(pdf_path)
    
    print(f"\nAnalysis complete! Report saved to: output/{result['file_title']}.md") 