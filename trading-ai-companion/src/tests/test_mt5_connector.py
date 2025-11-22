"""
Test MT5 Connector
"""

import unittest
from unittest.mock import Mock, patch
from src.modules.mt5_connector.mt5_manager import MT5Manager

class TestMT5Manager(unittest.TestCase):
    def setUp(self):
        self.mt5_manager = MT5Manager()
    
    def test_initialize_manager(self):
        """Test MT5 manager initialization"""
        self.assertIsNotNone(self.mt5_manager)
        self.assertFalse(self.mt5_manager.is_initialized)

if __name__ == '__main__':
    unittest.main()
