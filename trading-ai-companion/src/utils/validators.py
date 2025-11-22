"""
Data Validators
"""

import re
from typing import Any, Dict, List

def validate_currency_pair(symbol: str) -> bool:
    """Validate currency pair format (e.g., EURUSD)"""
    pattern = r'^[A-Z]{6}$'
    return bool(re.match(pattern, symbol))

def validate_timeframe(timeframe: str) -> bool:
    """Validate MT5 timeframe"""
    valid_timeframes = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN1']
    return timeframe in valid_timeframes

def validate_position_size(size: float) -> bool:
    """Validate position size"""
    return isinstance(size, (int, float)) and size > 0

def validate_risk_percent(risk: float) -> bool:
    """Validate risk percentage (0-100)"""
    return isinstance(risk, (int, float)) and 0 <= risk <= 100

def validate_config_structure(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """Validate configuration structure"""
    try:
        for key in required_keys:
            if key not in config:
                return False
            if isinstance(config[key], dict) and 'required' in config[key]:
                if not validate_config_structure(config[key], config[key]['required']):
                    return False
        return True
    except Exception:
        return False
