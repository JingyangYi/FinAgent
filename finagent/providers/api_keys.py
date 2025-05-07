"""
API keys management module.
Handles loading, storing, and retrieving API keys from a local file.
"""

import os
import json
from pathlib import Path

# Paths to check for API keys file
PROJECT_KEYS_FILE = Path("finagent_keys.json")  # In project directory
HOME_KEYS_FILE = Path.home() / ".finagent_keys.json"  # In home directory as fallback

def load_api_keys():
    """
    Load API keys from finagent_keys.json file and set them as environment variables.
    First checks in the project directory, then falls back to home directory.
    
    Returns:
        bool: True if API keys were loaded successfully, False otherwise
    """
    # First check if the file exists in the project directory
    if PROJECT_KEYS_FILE.exists():
        keys_file = PROJECT_KEYS_FILE
    # Then check if it exists in the home directory
    elif HOME_KEYS_FILE.exists():
        keys_file = HOME_KEYS_FILE
    else:
        # If no file exists, point to the project directory version
        keys_file = PROJECT_KEYS_FILE
        print(f"API keys file not found!")
        print(f"Please fill in your API keys in the finagent_keys.json file in the project directory.")
        print("You need at least one of DEEPSEEK_API_KEY or OPENAI_API_KEY, and TAVILY_API_KEY.")
        return False
    
    try:
        # Load keys from file
        with open(keys_file, "r") as f:
            keys = json.load(f)
        
        # Set keys as environment variables if they exist
        for key_name, key_value in keys.items():
            if key_value:  # Only set if the key has a value
                os.environ[key_name] = key_value
        
        # Check if all required keys are set
        missing_keys = []
        if not keys.get("DEEPSEEK_API_KEY") and not keys.get("OPENAI_API_KEY"):
            missing_keys.append("DEEPSEEK_API_KEY or OPENAI_API_KEY")
        if not keys.get("TAVILY_API_KEY"):
            missing_keys.append("TAVILY_API_KEY")
        
        if missing_keys:
            print(f"Missing API keys: {', '.join(missing_keys)}")
            print(f"Please add them to {keys_file} and restart the application.")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error loading API keys: {e}")
        return False

def get_api_key(key_name):
    """
    Get a specific API key from environment variables.
    
    Args:
        key_name: Name of the API key to retrieve
        
    Returns:
        API key value or None if not found
    """
    return os.environ.get(key_name) 