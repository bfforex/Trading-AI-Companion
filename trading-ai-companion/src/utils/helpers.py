"""
Helper Functions
"""

import json
import yaml
import os
from typing import Any, Dict
from datetime import datetime

def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """Load YAML file"""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return {}

def save_yaml_file(data: Dict[str, Any], file_path: str):
    """Save data to YAML file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
    except Exception as e:
        print(f"Error saving YAML file {file_path}: {e}")

def format_timestamp(timestamp: datetime = None) -> str:
    """Format timestamp for logging"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def safe_float_convert(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int_convert(value: Any, default: int = 0) -> int:
    """Safely convert value to int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
