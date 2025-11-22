"""
Portfolio Risk Manager
"""

import logging
from typing import Dict, List, Any

class PortfolioManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.positions = {}
        self.portfolio_stats = {}
    
    def update_position(self, symbol: str, position_data: Dict[str, Any]):
        """Update position information"""
        try:
            self.positions[symbol] = position_data
            self._recalculate_portfolio_stats()
        except Exception as e:
            self.logger.error(f"Error updating position: {e}")
    
    def remove_position(self, symbol: str):
        """Remove closed position"""
        try:
            if symbol in self.positions:
                del self.positions[symbol]
                self._recalculate_portfolio_stats()
        except Exception as e:
            self.logger.error(f"Error removing position: {e}")
    
    def _recalculate_portfolio_stats(self):
        """Recalculate portfolio statistics"""
        try:
            total_exposure = 0
            total_pnl = 0
            positions_by_currency = {}
            
            for symbol, position in self.positions.items():
                exposure = position.get('exposure', 0)
                pnl = position.get('pnl', 0)
                
                total_exposure += exposure
                total_pnl += pnl
                
                # Group by currency pair
                base_currency = symbol[:3]
                quote_currency = symbol[3:]
                currency_pair = f"{base_currency}/{quote_currency}"
                
                if currency_pair not in positions_by_currency:
                    positions_by_currency[currency_pair] = {
                        'exposure': 0,
                        'pnl': 0,
                        'count': 0
                    }
                
                positions_by_currency[currency_pair]['exposure'] += exposure
                positions_by_currency[currency_pair]['pnl'] += pnl
                positions_by_currency[currency_pair]['count'] += 1
            
            self.portfolio_stats = {
                'total_exposure': total_exposure,
                'total_pnl': total_pnl,
                'positions_count': len(self.positions),
                'positions_by_currency': positions_by_currency
            }
        except Exception as e:
            self.logger.error(f"Error recalculating portfolio stats: {e}")
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary statistics"""
        return self.portfolio_stats
    
    def check_correlation_risk(self, new_symbol: str) -> Dict[str, Any]:
        """Check correlation risk with existing positions"""
        try:
            # This would typically involve correlation matrix calculations
            # For now, we'll provide a basic implementation
            correlation_risk = {
                'risk_level': 'low',
                'similar_positions': [],
                'recommendation': 'proceed'
            }
            
            # Check for similar currency pairs
            new_base = new_symbol[:3]
            new_quote = new_symbol[3:]
            
            for existing_symbol in self.positions.keys():
                existing_base = existing_symbol[:3]
                existing_quote = existing_symbol[3:]
                
                # Check for same base or quote currency
                if new_base == existing_base or new_quote == existing_quote:
                    correlation_risk['similar_positions'].append(existing_symbol)
            
            if len(correlation_risk['similar_positions']) > 2:
                correlation_risk['risk_level'] = 'high'
                correlation_risk['recommendation'] = 'review'
            
            return correlation_risk
        except Exception as e:
            self.logger.error(f"Error checking correlation risk: {e}")
            return {
                'risk_level': 'unknown',
                'similar_positions': [],
                'recommendation': 'proceed'
            }
