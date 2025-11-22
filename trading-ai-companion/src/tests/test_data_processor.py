"""
Test Data Processor
"""

import unittest
from modules.data_processor.technical_indicators import TechnicalIndicators

class TestTechnicalIndicators(unittest.TestCase):
    def setUp(self):
        self.indicators = TechnicalIndicators()
    
    def test_calculate_rsi(self):
        """Test RSI calculation"""
        prices = [100, 101, 102, 101, 100, 99, 98, 99, 100, 101] * 2  # 20 prices
        rsi = self.indicators.calculate_rsi(prices, period=14)
        self.assertIsInstance(rsi, float)
        self.assertTrue(0 <= rsi <= 100)
    
    def test_calculate_macd(self):
        """Test MACD calculation"""
        prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109] * 3  # 30 prices
        macd_result = self.indicators.calculate_macd(prices)
        self.assertIn('macd', macd_result)
        self.assertIn('signal', macd_result)
        self.assertIn('histogram', macd_result)

if __name__ == '__main__':
    unittest.main()
