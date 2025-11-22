"""
Main Application Class - Updated with MT5 Integration
"""

import logging
import time
from typing import Optional, Dict, Any
from src.core.config_manager import ConfigManager
from src.modules.mt5_connector.mt5_manager import MT5Manager
from src.modules.mt5_connector.process_monitor import MT5ProcessMonitor
from src.modules.mt5_connector.api_client import MT5APIClient

class TradingAIApp:
    def __init__(self, config_path: Optional[str] = None, debug: bool = False):
        self.logger = logging.getLogger(__name__)
        self.debug = debug

        # Fallback to default config if none provided
        if config_path is None:
            default_path = Path(__file__).parent.parent / "config" / "config.yaml"
            config_path = str(default_path)

        # Load configuration
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config
        
        # Initialize core components
        self.mt5_manager = None
        self.mt5_monitor = MT5ProcessMonitor()
        self.is_running = False
        
        self.logger.info("Trading AI Companion App initialized")
    
    def initialize_mt5(self) -> bool:
        """Initialize MT5 connection"""
        try:
            mt5_config = self.config.get('mt5', {})
            self.mt5_manager = MT5Manager(mt5_config)
            
            success = self.mt5_manager.initialize()
            if success:
                self.logger.info("MT5 initialized successfully")
            else:
                self.logger.error("Failed to initialize MT5")
            
            return success
        except Exception as e:
            self.logger.error(f"Error initializing MT5: {e}")
            return False
    
    def start_core_services(self) -> bool:
        """Start core application services"""
        try:
            # Initialize MT5 first (most critical)
            if not self.initialize_mt5():
                self.logger.error("Failed to initialize MT5 - critical service")
                return False
            
            # Initialize other services here as they're implemented
            # self.ai_orchestrator = AIOrchestrator()
            # self.risk_engine = RiskEngine()
            # self.market_analyzer = MarketAnalyzer()
            
            self.is_running = True
            self.logger.info("Core services started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting core services: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'app_status': 'running' if self.is_running else 'stopped',
            'timestamp': time.time(),
            'services': {}
        }
        
        # MT5 Status
        if self.mt5_manager:
            status['services']['mt5'] = {
                'initialized': self.mt5_manager.is_initialized,
                'system_info': self.mt5_manager.get_system_info()
            }
        
        # Process Monitor Status
        try:
            status['process_monitor'] = {
                'mt5_processes': self.mt5_monitor.get_mt5_process_stats(),
                'system_resources': self.mt5_monitor.get_system_resources(),
                'resource_alerts': self.mt5_monitor.check_resource_thresholds()
            }
        except Exception as e:
            status['process_monitor'] = {'error': str(e)}
        
        return status
    
    def get_account_summary(self) -> Dict[str, Any]:
        """Get account summary information"""
        if not self.mt5_manager or not self.mt5_manager.is_initialized:
            return {'error': 'MT5 not initialized'}
        
        try:
            account_info = self.mt5_manager.get_account_info()
            positions = self.mt5_manager.get_positions()
            
            return {
                'account_info': account_info,
                'positions_count': len(positions),
                'total_positions': positions,
                'timestamp': time.time()
            }
        except Exception as e:
            self.logger.error(f"Error getting account summary: {e}")
            return {'error': str(e)}
    
    def place_test_order(self, symbol: str, order_type: str, volume: float) -> Dict[str, Any]:
        """Place a test order"""
        if not self.mt5_manager or not self.mt5_manager.is_initialized:
            return {'error': 'MT5 not initialized'}
        
        try:
            result = self.mt5_manager.place_order(symbol, order_type, volume, comment="Test order")
            return result
        except Exception as e:
            self.logger.error(f"Error placing test order: {e}")
            return {'error': str(e)}
    
    def shutdown(self):
        """Shutdown the application gracefully"""
        self.logger.info("Shutting down Trading AI Companion App")
        
        # Shutdown MT5
        if self.mt5_manager:
            self.mt5_manager.shutdown()
        
        self.is_running = False
        self.logger.info("Application shutdown complete")
