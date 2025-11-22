#!/usr/bin/env python3
"""
Test if MT5 is running on the system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_mt5_running():
    print("Testing if MT5 is running...")
    print("=" * 40)
    
    try:
        from src.modules.mt5_connector.process_monitor import MT5ProcessMonitor
        monitor = MT5ProcessMonitor()
        
        # Find MT5 processes
        mt5_processes = monitor.find_mt5_processes()
        
        if mt5_processes:
            print(f"✅ MT5 is running! Found {len(mt5_processes)} process(es):")
            for proc in mt5_processes:
                print(f"   PID: {proc.get('pid')}, Name: {proc.get('name')}")
                if proc.get('exe'):
                    print(f"   Path: {proc.get('exe')}")
            return True
        else:
            print("❌ MT5 is not running")
            print("\nTo test with MT5:")
            print("1. Launch MetaTrader 5 terminal")
            print("2. Run this script again")
            return False
            
    except Exception as e:
        print(f"❌ Error checking MT5 processes: {e}")
        return False

def test_mt5_manager_detection():
    print("\nTesting MT5 Manager detection...")
    print("=" * 40)
    
    try:
        from modules.mt5_connector.mt5_manager import MT5Manager
        
        # Create manager with config that doesn't auto-launch
        config = {
            'auto_launch': False,
            'api_base_url': 'http://localhost:8082'
        }
        manager = MT5Manager(config)
        
        # Check if MT5 is running
        is_running = manager._is_mt5_running()
        print(f"MT5 running status: {is_running}")
        
        # Get system info
        system_info = manager.get_system_info()
        print(f"MT5 executable path: {system_info.get('mt5_executable', 'Not found')}")
        print(f"Process running: {system_info.get('mt5_process_running', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in MT5 manager test: {e}")
        return False

if __name__ == "__main__":
    print("MT5 Running Test")
    print("=" * 20)
    
    success1 = test_mt5_running()
    success2 = test_mt5_manager_detection()
    
    if success1 and success2:
        print("\n🎉 MT5 detection working perfectly!")
    else:
        print("\n⚠️  MT5 not detected or issues found")
