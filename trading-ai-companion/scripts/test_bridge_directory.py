#!/usr/bin/env python3
"""
Test Bridge Directory Access
"""

import os
import platform
from pathlib import Path

def test_bridge_access():
    print("Testing Bridge Directory Access")
    print("=" * 40)
    
    # Determine bridge path
    system = platform.system()
    if system == "Windows":
        bridge_path = os.path.expanduser("~/AppData/Local/TradingAI/mt5_bridge")
    else:
        bridge_path = os.path.expanduser("~/.tradingai/mt5_bridge")
    
    print(f"Target bridge path: {bridge_path}")
    
    # Check if path exists
    if os.path.exists(bridge_path):
        print("✓ Bridge directory exists")
    else:
        print("⚠ Bridge directory does not exist")
        try:
            # Try to create it
            Path(bridge_path).mkdir(parents=True, exist_ok=True)
            print("✓ Bridge directory created successfully")
        except Exception as e:
            print(f"❌ Failed to create bridge directory: {e}")
            return False
    
    # Test write access
    test_file = os.path.join(bridge_path, "access_test.txt")
    try:
        with open(test_file, 'w') as f:
            f.write("Test successful!")
        print("✓ Write access working")
        
        # Test read access
        with open(test_file, 'r') as f:
            content = f.read()
        print("✓ Read access working")
        print(f"  Content: {content}")
        
        # Cleanup
        os.remove(test_file)
        print("✓ Cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ File access failed: {e}")
        return False

if __name__ == "__main__":
    success = test_bridge_access()
    if success:
        print("\n🎉 Bridge directory is ready for use!")
    else:
        print("\n❌ Bridge directory has issues that need fixing.")
