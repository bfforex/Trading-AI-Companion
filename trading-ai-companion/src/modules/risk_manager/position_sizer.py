"""
Position Sizing Calculator
"""

import logging
from typing import Dict, Any

class PositionSizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def kelly_criterion(self, win_rate: float, win_loss_ratio: float) -> float:
        """Calculate position size using Kelly Criterion"""
        try:
            if win_loss_ratio <= 0:
                return 0.0
            
            kelly = win_rate - ((1 - win_rate) / win_loss_ratio)
            return max(0.0, min(kelly, 1.0))  # Clamp between 0 and 1
        except Exception as e:
            self.logger.error(f"Error calculating Kelly Criterion: {e}")
            return 0.0
    
    def fixed_fractional(self, account_balance: float, risk_percent: float) -> float:
        """Calculate position size using fixed fractional method"""
        try:
            return account_balance * (risk_percent / 100)
        except Exception as e:
            self.logger.error(f"Error calculating fixed fractional: {e}")
            return 0.0
    
    def volatility_adjusted(self, account_balance: float, atr: float, risk_percent: float, pip_value: float) -> float:
        """Calculate position size adjusted for volatility"""
        try:
            if atr <= 0 or pip_value <= 0:
                return 0.0
            
            risk_amount = account_balance * (risk_percent / 100)
            position_size = risk_amount / (atr * pip_value)
            return round(position_size, 2)
        except Exception as e:
            self.logger.error(f"Error calculating volatility adjusted position size: {e}")
            return 0.0
