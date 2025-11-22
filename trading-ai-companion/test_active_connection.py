#!/usr/bin/env python3
"""
Test Active MT5 Connection
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_active_connection():
    print("Testing Active MT5 Connection...")
    print("=" * 40)
    
    try:
        from src.modules.mt5_connector.api_client import MT5APIClient
        client = MT5APIClient(base_url="http://localhost:8082")
        
        print("1. Testing server ping...")
        try:
            response = client.ping()
            print(f"   Ping result: {response}")
        except Exception as e:
            print(f"   Ping failed: {e}")
        
        print("2. Testing server status...")
        try:
            status = client.get_server_status()
            print(f"   Status: {status}")
        except Exception as e:
            print(f"   Status check failed: {e}")
        
        print("3. Testing account info...")
        try:
            account = client.get_account_info()
            print(f"   Account info: {account}")
        except Exception as e:
            print(f"   Account info failed: {e}")
        
        print("4. Testing market data...")
        try:
            market_data = client.get_market_data("EURUSD", "M1", 10)
            print(f"   Market data received: {len(market_data.get('bars', []))} bars")
        except Exception as e:
            print(f"   Market data failed: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("Active MT5 Connection Test")
    print("=" * 30)
    test_active_connection()
