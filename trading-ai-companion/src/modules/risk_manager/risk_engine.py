"""
Risk Management Engine
"""

import logging
from typing import Dict, Any

class RiskEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.risk_limits = {}
        self.portfolio_exposure = {}
    
    def set_risk_limits(self, limits: Dict[str, Any]):
        """Set risk management limits"""
        self.risk_limits = limits
        self.logger.info("Risk limits updated")
    
    def calculate_position_size(self, account_balance: float, risk_per_trade: float, stop_loss_pips: float, pip_value: float) -> float:
        """Calculate optimal position size based on risk parameters"""
        try:
            # Risk amount in currency
            risk_amount = account_balance * risk_per_trade
            
            # Position size calculation
            if stop_loss_pips > 0 and pip_value > 0:
                position_size = risk_amount / (stop_loss_pips * pip_value)
                return round(position_size, 2)
            else:
                return 0.0
        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0.0
    
    def check_trade_risk(self, symbol: str, position_size: float, account_balance: float) -> Dict[str, Any]:
        """Check if a trade complies with risk rules"""
        try:
            # Check maximum position size
            max_position_value = account_balance * self.risk_limits.get('max_position_size', 0.02)
            
            # Check symbol exposure
            current_exposure = self.portfolio_exposure.get(symbol, 0)
            max_symbol_exposure = self.risk_limits.get('max_exposure_per_pair', 0.05) * account_balance
            
            compliance = {
                'compliant': True,
                'violations': []
            }
            
            if position_size > max_position_value:
                compliance['compliant'] = False
                compliance['violations'].append('Position size exceeds maximum limit')
            
            if (current_exposure + position_size) > max_symbol_exposure:
                compliance['compliant'] = False
                compliance['violations'].append('Symbol exposure exceeds maximum limit')
            
            return compliance
        except Exception as e:
            self.logger.error(f"Error checking trade risk: {e}")
            return {'compliant': False, 'violations': ['System error']}
