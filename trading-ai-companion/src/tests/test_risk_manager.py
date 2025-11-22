"""
Test Risk Manager
"""

import unittest
from modules.risk_manager.risk_engine import RiskEngine

class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        self.risk_engine = RiskEngine()
    
    def test_calculate_position_size(self):
        """Test position size calculation"""
        position_size = self.risk_engine.calculate_position_size(
            account_balance=10000,
            risk_per_trade=0.01,
            stop_loss_pips=50,
            pip_value=10
        )
        expected_size = (10000 * 0.01) / (50 * 10)  # 0.2
        self.assertAlmostEqual(position_size, expected_size, places=2)
    
    def test_set_risk_limits(self):
        """Test setting risk limits"""
        limits = {'max_position_size': 0.02, 'max_daily_loss': 0.05}
        self.risk_engine.set_risk_limits(limits)
        self.assertEqual(self.risk_engine.risk_limits, limits)

if __name__ == '__main__':
    unittest.main()
