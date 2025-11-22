#!/usr/bin/env python3
"""
Manual Test Script for Phase 1
"""

import sys
import os
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.app import TradingAIApp
from src.utils.logger import setup_logger

def manual_test():
    """Run manual tests for Phase 1 functionality"""
    print("=" * 60)
    print("Trading AI Companion - Phase 1 Manual Test")
    print("=" * 60)
    
    # Setup logging
    logger = setup_logger("ManualTest", "logs/manual_test.log")
    logger.info("Starting manual test")
    
    try:
        print("\n1. Testing Application Initialization...")
        app = TradingAIApp(config_path="config/config.yaml", debug=True)
        print("   ✓ Application created successfully")
        
        print("\n2. Testing System Status...")
        status = app.get_system_status()
        print(f"   ✓ System status retrieved")
        print(f"   App Status: {status['app_status']}")
        print(f"   Services: {list(status['services'].keys())}")
        
        print("\n3. Testing Configuration...")
        if app.config:
            print(f"   ✓ Configuration loaded")
            print(f"   Config sections: {list(app.config.keys())}")
        else:
            print("   ⚠ No configuration loaded")
        
        print("\n4. Testing MT5 Manager (without actual MT5)...")
        # Test MT5 manager initialization
        from src.modules.mt5_connector.mt5_manager import MT5Manager
        mt5_manager = MT5Manager()
        system_info = mt5_manager.get_system_info()
        print(f"   ✓ MT5 Manager created")
        print(f"   MT5 Executable: {system_info['mt5_executable'] or 'Not found'}")
        print(f"   Initialized: {system_info['is_initialized']}")
        
        print("\n5. Testing Process Monitor...")
        from src.modules.mt5_connector.process_monitor import MT5ProcessMonitor
        monitor = MT5ProcessMonitor()
        
        # System resources
        resources = monitor.get_system_resources()
        print(f"   ✓ System resources monitored")
        print(f"   CPU: {resources.get('cpu_percent', 0):.1f}%")
        print(f"   Memory: {resources.get('memory', {}).get('percent', 0):.1f}%")
        
        # Process detection
        processes = monitor.find_mt5_processes()
        print(f"   ✓ Process detection completed")
        print(f"   MT5 Processes found: {len(processes)}")
        
        print("\n6. Testing API Client...")
        from src.modules.mt5_connector.api_client import MT5APIClient
        api_client = MT5APIClient()
        print(f"   ✓ API Client created")
        print(f"   Base URL: {api_client.base_url}")
        
        print("\n7. Testing Logger...")
        logger.info("Manual test log entry")
        print(f"   ✓ Logger working - entry written to logs/manual_test.log")
        
        print("\n" + "=" * 60)
        print("MANUAL TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review logs in logs/ directory")
        print("2. Run automated tests with: python scripts/run_tests.py")
        print("3. Test CLI interface: python src/main.py --help")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Manual test failed: {e}")
        logger.error(f"Manual test failed: {e}")
        return False

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    
    success = manual_test()
    sys.exit(0 if success else 1)
