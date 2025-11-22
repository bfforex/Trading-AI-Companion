"""
MT5 Manager - Optimal Implementation with Multiple Communication Methods
"""

import os
import time
import psutil
import logging
import platform
import subprocess
from typing import Dict, Any, List, Optional
from src.modules.mt5_connector.zmq_bridge import MT5ZMQBridge  # Best option
from src.modules.mt5_connector.api_client import MT5APIClient  # Fallback

class MT5Manager:
    def __init__(self, config: Dict = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        self.is_initialized = False
        self.mt5_executable = self._get_mt5_executable_path()
        
        # Communication priority: ZMQ > API > Bridge
        self.communication_method = None
        self.zmq_bridge = None
        self.api_client = None
        
        # Initialize based on configuration
        self._initialize_communication()
    
    def _initialize_communication(self):
        """Initialize communication method based on availability"""
        # Try ZMQ first (best performance)
        if self._try_zmq():
            self.communication_method = 'zmq'
            return
            
        # Try REST API as fallback
        if self._try_api():
            self.communication_method = 'api'
            return
            
        # If neither works, we can't communicate
        self.logger.error("No communication method available")
    
    def _try_zmq(self) -> bool:
        """Try to initialize ZMQ communication"""
        try:
            port = self.config.get('zmq_port', 5555)
            host = self.config.get('zmq_host', 'localhost')
            
            self.zmq_bridge = MT5ZMQBridge(port=port, host=host)
            self.zmq_bridge.connect_client()
            
            # Test connection
            test_response = self.zmq_bridge.send_request('ping', timeout=50000)
            if test_response.get('success', False):
                self.logger.info("ZMQ communication established")
                return True
            else:
                self.zmq_bridge.close()
                self.zmq_bridge = None
                return False
                
        except Exception as e:
            self.logger.debug(f"ZMQ not available: {e}")
            if self.zmq_bridge:
                self.zmq_bridge.close()
                self.zmq_bridge = None
            return False
    
    def _try_api(self) -> bool:
        """Try to initialize REST API communication"""
        try:
            api_base_url = self.config.get('api_base_url', 'http://localhost:8082')
            self.api_client = MT5APIClient(base_url=api_base_url)
            
            # Test connection
            status = self.api_client.get_server_status()
            if status.get('status') == 'connected':
                self.logger.info("REST API communication established")
                return True
            else:
                self.api_client = None
                return False
                
        except Exception as e:
            self.logger.debug(f"REST API not available: {e}")
            self.api_client = None
            return False
    
    def _get_mt5_executable_path(self) -> str:
        """Get MT5 executable path"""
        custom_path = self.config.get('mt5_executable_path')
        if custom_path and os.path.exists(custom_path):
            return custom_path
        
        system = platform.system()
        paths = {
            "Windows": [
                "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
                "C:\\Program Files (x86)\\MetaTrader 5\\terminal64.exe"
            ],
            "Darwin": ["/Applications/MetaTrader 5.app/Contents/MacOS/MetaTrader 5"],
            "Linux": ["/opt/metatrader5/terminal64.exe"]
        }
        
        for path in paths.get(system, []):
            if os.path.exists(path):
                return path
        return ""
    
    def initialize(self) -> bool:
        """Initialize MT5 with optimal communication method"""
        try:
            self.logger.info("Initializing MT5 with optimal communication")
            
            # Ensure MT5 is running
            if not self._ensure_mt5_running():
                return False
            
            # Initialize communication (already done in __init__)
            if not self.communication_method:
                self._initialize_communication()
            
            if not self.communication_method:
                self.logger.error("No communication method available")
                return False
            
            # Verify connection
            if self._verify_connection():
                self.is_initialized = True
                self.logger.info(f"MT5 initialized with {self.communication_method} communication")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Error initializing MT5: {e}")
            return False
    
    def _ensure_mt5_running(self) -> bool:
        """Ensure MT5 is running"""
        if self._is_mt5_running():
            return True
        
        if not self.config.get('auto_launch', True):
            self.logger.error("MT5 not running and auto-launch disabled")
            return False
        
        return self._launch_mt5()
    
    def _is_mt5_running(self) -> bool:
        """Check if MT5 is running"""
        for proc in psutil.process_iter(['name']):
            try:
                if 'terminal' in proc.info['name'].lower() and 'meta' in proc.info['name'].lower():
                    return True
            except:
                continue
        return False
    
    def _launch_mt5(self) -> bool:
        """Launch MT5 application"""
        if not self.mt5_executable or not os.path.exists(self.mt5_executable):
            self.logger.error("MT5 executable not found")
            return False
        
        try:
            subprocess.Popen([self.mt5_executable])
            time.sleep(10)  # Wait for MT5 to start
            return True
        except Exception as e:
            self.logger.error(f"Failed to launch MT5: {e}")
            return False
    
    def _verify_connection(self) -> bool:
        """Verify communication is working"""
        try:
            status = self.get_server_status()
            return status.get('status') == 'connected'
        except Exception as e:
            self.logger.error(f"Connection verification failed: {e}")
            return False
    
    def _send_request(self, command: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send request using the best available method"""
        if not self.is_initialized:
            return {'error': 'MT5 not initialized', 'success': False}
        
        try:
            if self.communication_method == 'zmq' and self.zmq_bridge:
                return self.zmq_bridge.send_request(command, data)
            elif self.communication_method == 'api' and self.api_client:
                # Map commands to API calls
                return self._map_command_to_api(command, data)
            else:
                return {'error': 'No communication method available', 'success': False}
        except Exception as e:
            self.logger.error(f"Error sending request: {e}")
            return {'error': str(e), 'success': False}
    
    def _map_command_to_api(self, command: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Map internal commands to REST API calls"""
        # This would map our internal command structure to the REST API
        # Implementation depends on the specific REST API being used
        pass
    
    # Public methods (same interface regardless of communication method)
    def get_server_status(self) -> Dict[str, Any]:
        return self._send_request('get_status')
    
    def get_account_info(self) -> Dict[str, Any]:
        return self._send_request('get_account_info')
    
    def get_market_data(self, symbol: str, timeframe: str = "M1", count: int = 100) -> Dict[str, Any]:
        data = {'symbol': symbol, 'timeframe': timeframe, 'count': count}
        return self._send_request('get_market_data', data)
    
    def place_order(self, symbol: str, order_type: str, volume: float, price: float = None,
                   sl: float = None, tp: float = None, comment: str = "") -> Dict[str, Any]:
        data = {
            'symbol': symbol, 'type': order_type, 'volume': volume,
            'price': price, 'sl': sl, 'tp': tp, 'comment': comment
        }
        return self._send_request('place_order', data)
    
    def get_positions(self) -> List[Dict[str, Any]]:
        response = self._send_request('get_positions')
        return response.get('positions', [])
    
    def close_position(self, ticket: int) -> Dict[str, Any]:
        return self._send_request('close_position', {'ticket': ticket})
    
    def shutdown(self):
        """Shutdown gracefully"""
        try:
            if self.zmq_bridge:
                self.zmq_bridge.close()
            self.is_initialized = False
            self.logger.info("MT5 connection shut down")
        except Exception as e:
            self.logger.error(f"Error shutting down: {e}")
