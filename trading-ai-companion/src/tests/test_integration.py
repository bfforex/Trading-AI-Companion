"""
Integration Tests for Phase 1
"""

import sys
import os
import unittest
from pathlib import Path
import tempfile
import json

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from core.app import TradingAIApp
from utils.logger import setup_logger

class TestPhase1Integration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests in the class."""
        # Setup test logging
        cls.test_log_file = "logs/test_integration.log"
        cls.logger = setup_logger("IntegrationTest", cls.test_log_file)
    
    def test_app_initialization(self):
        """Test complete application initialization"""
        try:
            # Create minimal config for testing
            test_config = {
                'app': {'debug': True},
                'mt5': {
                    'auto_launch': False,
                    'api_base_url': 'http://localhost:8082'
                }
            }
            
            # Write test config to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                import yaml
                yaml.dump(test_config, f)
                config_path = f.name
            
            # Initialize app
            app = TradingAIApp(config_path=config_path, debug=True)
            
            self.assertIsNotNone(app)
            self.assertIsNotNone(app.config_manager)
            print("✓ Application initialization successful")
            
            # Cleanup
            os.unlink(config_path)
            
        except Exception as e:
            self.fail(f"Application initialization failed: {e}")
    
    def test_system_status(self):
        """Test system status without MT5 initialization"""
        try:
            app = TradingAIApp(debug=True)
            status = app.get_system_status()
            
            self.assertIsInstance(status, dict)
            self.assertIn('app_status', status)
            self.assertIn('services', status)
            print("✓ System status retrieval working")
            print(f"  App status: {status['app_status']}")
            
        except Exception as e:
            self.fail(f"System status test failed: {e}")
    
    def test_configuration_loading(self):
        """Test configuration loading from default config"""
        try:
            app = TradingAIApp(debug=True)
            
            # Check that config was loaded
            self.assertIsNotNone(app.config)
            self.assertIsInstance(app.config, dict)
            
            # Check for expected config sections
            self.assertIn('app', app.config)
            self.assertIn('mt5', app.config)
            self.assertIn('ai', app.config)
            
            print("✓ Configuration loading working")
            print(f"  Config sections: {list(app.config.keys())}")
            
        except Exception as e:
            self.fail(f"Configuration loading test failed: {e}")

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    unittest.main()
