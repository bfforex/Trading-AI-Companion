#!/usr/bin/env python3
"""
Debug MT5 API Client Issues
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_api_client():
    print("Testing MT5 API Client...")
    print("=" * 40)
    
    try:
        # Import the API client
        print("1. Importing MT5APIClient...")
        from src.modules.mt5_connector.api_client import MT5APIClient
        print("   ✓ Import successful")
        
        # Create client instance
        print("2. Creating API client instance...")
        client = MT5APIClient(base_url="http://localhost:8082")
        print("   ✓ Client created")
        print(f"   Base URL: {client.base_url}")
        
        # Test basic methods
        print("3. Testing client methods...")
        print(f"   Session type: {type(client.session)}")
        print(f"   Has _make_request method: {hasattr(client, '_make_request')}")
        print(f"   Has get_server_status method: {hasattr(client, 'get_server_status')}")
        
        # Test ping method (if it exists)
        print("4. Testing connection...")
        if hasattr(client, 'ping'):
            try:
                result = client.ping()
                print(f"   Ping result: {result}")
            except Exception as e:
                print(f"   Ping failed (expected if MT5 not running): {e}")
        else:
            print("   No ping method found")
        
        print("\n✓ API Client basic functionality working!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if src/modules/mt5_connector/api_client.py exists")
        print("2. Verify file permissions")
        print("3. Check Python path")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_file_structure():
    """Check if required files exist"""
    print("\nChecking file structure...")
    print("=" * 40)
    
    required_files = [
        "src/modules/mt5_connector/api_client.py",
        "src/modules/mt5_connector/mt5_manager.py",
        "src/modules/mt5_connector/process_monitor.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")

if __name__ == "__main__":
    check_file_structure()
    print()
    test_api_client()
