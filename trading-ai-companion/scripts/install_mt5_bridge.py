#!/usr/bin/env python3
"""
MT5 Bridge Installation Script
"""

import os
import sys
import platform
from pathlib import Path

def install_mt5_bridge():
    """Install MT5 bridge components"""
    print("Installing MT5 Bridge...")
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    print(f"Project root: {project_root}")
    
    # Determine system-specific paths
    system = platform.system()
    
    if system == "Windows":
        # Windows installation
        bridge_path = os.path.expanduser("~/AppData/Local/TradingAI/mt5_bridge")
        mt5_data_path = os.path.expanduser("~/AppData/Roaming/MetaQuotes/Terminal")
    elif system == "Darwin":  # macOS
        bridge_path = os.path.expanduser("~/Library/Application Support/TradingAI/mt5_bridge")
        mt5_data_path = os.path.expanduser("~/Library/Application Support/MetaQuotes/Terminal")
    else:  # Linux
        bridge_path = os.path.expanduser("~/.tradingai/mt5_bridge")
        mt5_data_path = os.path.expanduser("~/.wine/drive_c/Program Files/MetaTrader 5")
    
    # Create bridge directory
    Path(bridge_path).mkdir(parents=True, exist_ok=True)
    print(f"Bridge directory created: {bridge_path}")
    
    # Create sample configuration
    config_content = f"""
# MT5 Bridge Configuration
bridge_path: "{bridge_path.replace(chr(92), chr(92)+chr(92))}"  # Double backslashes for YAML
communication_method: "bridge"
mt5:
  auto_launch: true
  mt5_executable_path: ""
  api_base_url: "http://localhost:8082"
  connection_timeout: 30
"""
    
    # Create config directory if it doesn't exist
    config_dir = project_root / "config"
    config_dir.mkdir(exist_ok=True)
    
    # Create config file
    config_file = config_dir / "mt5_bridge_config.yaml"
    try:
        with open(config_file, 'w') as f:
            f.write(config_content.strip())
        print(f"Bridge configuration created: {config_file}")
    except Exception as e:
        print(f"Warning: Could not create config file: {e}")
        print("Configuration content:")
        print(config_content)
    
    print("\nNext steps:")
    print("1. Copy the MQL5 Expert Advisor to your MT5 Experts folder")
    print("2. Attach the EA to a chart in MT5")
    print("3. Configure the bridge path in MT5 EA to match:", bridge_path)
    print("4. Start the Trading AI Companion with bridge configuration")
    
    # Also create a simple test script
    test_script = project_root / "test_bridge.py"
    test_content = f'''
#!/usr/bin/env python3
"""
Test MT5 Bridge
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_bridge():
    print("Testing MT5 Bridge...")
    print("Bridge path:", "{bridge_path}")
    
    import os
    if os.path.exists("{bridge_path}"):
        print("✓ Bridge directory exists")
        files = os.listdir("{bridge_path}")
        print(f"Files in bridge directory: {files}")
    else:
        print("❌ Bridge directory not found")

if __name__ == "__main__":
    test_bridge()
'''
    
    try:
        with open(test_script, 'w') as f:
            f.write(test_content.strip())
        print(f"Test script created: {test_script}")
    except Exception as e:
        print(f"Could not create test script: {e}")

if __name__ == "__main__":
    install_mt5_bridge()
