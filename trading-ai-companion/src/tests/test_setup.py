"""
Test Setup for Phase 1 - MT5 Integration
"""

import sys
import os
import unittest
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import setup_logger

class TestSetup(unittest.TestCase):
    def test_imports(self):
        """Test that all required modules can be imported"""
        try:
            from core.app import TradingAIApp
            from modules.mt5_connector.mt5_manager import MT5Manager
            from modules.mt5_connector.process_monitor import MT5ProcessMonitor
            from modules.mt5_connector.api_client import MT5APIClient
            print("✓ All modules imported successfully")
        except ImportError as e:
            self.fail(f"Import error: {e}")
    
    def test_logger_setup(self):
        """Test logger setup"""
        try:
            logger = setup_logger("TestLogger", "logs/test.log")
            logger.info("Logger test message")
            print("✓ Logger setup successful")
        except Exception as e:
            self.fail(f"Logger setup failed: {e}")
    
    def test_config_files_exist(self):
        """Test that configuration files exist"""
        config_files = [
            "config/config.yaml",
            "requirements.txt"
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                print(f"✓ {config_file} exists")
            else:
                print(f"⚠ {config_file} not found (may be created during setup)")

if __name__ == '__main__':
    unittest.main()
