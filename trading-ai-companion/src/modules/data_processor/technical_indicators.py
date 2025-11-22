"""
Technical Indicators Calculator
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any

class TechnicalIndicators:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        try:
            deltas = np.diff(prices)
            gains = deltas.copy()
            losses = deltas.copy()
            gains[gains < 0] = 0
            losses[losses > 0] = 0
            
            avg_gain = np.mean(gains[-period:])
            avg_loss = abs(np.mean(losses[-period:]))
            
            if avg_loss == 0:
                return 100
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            self.logger.error(f"Error calculating RSI: {e}")
            return 50.0
    
    def calculate_macd(self, prices: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, float]:
        """Calculate MACD indicator"""
        try:
            prices_series = pd.Series(prices)
            ema_fast = prices_series.ewm(span=fast_period).mean()
            ema_slow = prices_series.ewm(span=slow_period).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal_period).mean()
            histogram = macd_line - signal_line
            
            return {
                'macd': float(macd_line.iloc[-1]),
                'signal': float(signal_line.iloc[-1]),
                'histogram': float(histogram.iloc[-1])
            }
        except Exception as e:
            self.logger.error(f"Error calculating MACD: {e}")
            return {'macd': 0, 'signal': 0, 'histogram': 0}
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, std_dev: int = 2) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        try:
            prices_series = pd.Series(prices)
            sma = prices_series.rolling(window=period).mean()
            std = prices_series.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            return {
                'upper': float(upper_band.iloc[-1]),
                'middle': float(sma.iloc[-1]),
                'lower': float(lower_band.iloc[-1])
            }
        except Exception as e:
            self.logger.error(f"Error calculating Bollinger Bands: {e}")
            return {'upper': 0, 'middle': 0, 'lower': 0}
