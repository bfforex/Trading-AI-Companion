"""
Test MT5 Manager
"""

import sys
import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.modules.mt5_connector.mt5_manager import MT5Manager

class TestMT5Manager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create minimal config for testing
        self.test_config = {
            'auto_launch': False,  # Don't auto-launch in tests
            'mt5_executable_path': '',
            'api_base_url': 'http://localhost:8082',
            'communication_method': 'api'
        }
        self.manager = MT5Manager(self.test_config)
    
    def test_initialization(self):
        """Test MT5Manager initialization"""
        self.assertIsNotNone(self.manager)
        self.assertIsInstance(self.manager, MT5Manager)
        print("✓ MT5Manager initialized successfully")
    
    def test_config_loading(self):
        """Test configuration loading"""
        self.assertEqual(self.manager.config, self.test_config)
        print("✓ Configuration loading working")
    
    def test_mt5_executable_detection(self):
        """Test MT5 executable path detection"""
        path = self.manager._get_mt5_executable_path()
        self.assertIsInstance(path, str)
        print(f"✓ MT5 executable detection working - path: {path or 'Not found'}")
    
    @patch('modules.mt5_connector.mt5_manager.psutil.process_iter')
    def test_process_detection(self, mock_process_iter):
        """Test MT5 process detection"""
        # Mock process data
        mock_process = Mock()
        mock_process.info = {
            'pid': 1234,
            'name': 'terminal.exe',
            'exe': 'C:\\Program Files\\MetaTrader 5\\terminal64.exe'
        }
        mock_process_iter.return_value = [mock_process]
        
        result = self.manager._is_mt5_running()
        self.assertIsInstance(result, bool)
        print("✓ Process detection mocking working")
    
    def test_system_info(self):
        """Test system information retrieval"""
        info = self.manager.get_system_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('mt5_executable', info)
        self.assertIn('is_initialized', info)
        self.assertIn('mt5_process_running', info)
        
        print("✓ System information retrieval working")
        print(f"  Initialized: {info['is_initialized']}")
        print(f"  Process running: {info['mt5_process_running']}")
    
    @patch('modules.mt5_connector.mt5_manager.MT5APIClient')
    def test_api_client_initialization(self, mock_api_client):
        """Test API client initialization"""
        # Mock the API client
        mock_instance = Mock()
        mock_api_client.return_value = mock_instance
        
        # Create new manager to trigger API client creation
        manager = MT5Manager(self.test_config)
        
        # Verify API client was created
        mock_api_client.assert_called()
        print("✓ API client initialization working")

if __name__ == '__main__':
    unittest.main()
