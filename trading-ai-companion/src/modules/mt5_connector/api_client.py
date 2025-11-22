"""
MT5 REST API Client - Complete Implementation
"""

import requests
import logging
import json
import time
from typing import Dict, Any, List, Optional
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class MT5APIError(Exception):
    """Custom exception for MT5 API client errors."""
    pass

class MT5APIClient:
    def __init__(self, base_url: str = "http://localhost:8082", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        
        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Authentication
        self.api_key = None
        self.authenticated = False
    
    def set_api_key(self, api_key: str):
        """Set API key for authentication"""
        self.api_key = api_key
        self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Add timeout to kwargs if not present
            if 'timeout' not in kwargs:
                kwargs['timeout'] = self.timeout
            
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Handle empty responses
            if not response.content:
                return {}
            
            return response.json()

        except ValueError as e:  # covers JSON decode errors

            self.logger.error(f"Invalid JSON response from {url}: {e}\nRaw: {response.text}")
            raise MT5APIError(f"Invalid API response: {str(e)}") from e
                   
        except Exception as e:
            self.logger.error(f"API request failed {method} {url}: {e}")
            raise MT5APIError(f"API request failed: {str(e)}") from e

    
    def get_server_status(self) -> Dict[str, Any]:
        """Get MT5 server status"""
        try:
            return self._make_request('GET', '/api/v1/status')
        except Exception as e:
            self.logger.error(f"Failed to get server status: {e}")
            return {'status': 'disconnected', 'error': str(e)}
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        try:
            return self._make_request('GET', '/api/v1/account')
        except Exception as e:
            self.logger.error(f"Failed to get account info: {e}")
            return {}
    
    def get_account_balance(self) -> float:
        """Get account balance"""
        try:
            account_info = self.get_account_info()
            return float(account_info.get('balance', 0))
        except Exception as e:
            self.logger.error(f"Failed to get account balance: {e}")
            return 0.0
    
    def get_account_equity(self) -> float:
        """Get account equity"""
        try:
            account_info = self.get_account_info()
            return float(account_info.get('equity', 0))
        except Exception as e:
            self.logger.error(f"Failed to get account equity: {e}")
            return 0.0
    
    def get_market_data(self, symbol: str, timeframe: str = "M1", count: int = 100) -> Dict[str, Any]:
        """Get market data for a symbol"""
        try:
            params = {
                'symbol': symbol.upper(),
                'timeframe': timeframe.upper(),
                'count': count
            }
            return self._make_request('GET', '/api/v1/market/data', params=params)
        except Exception as e:
            self.logger.error(f"Failed to get market data for {symbol}: {e}")
            return {}
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get symbol information"""
        try:
            params = {'symbol': symbol.upper()}
            return self._make_request('GET', '/api/v1/market/symbol', params=params)
        except Exception as e:
            self.logger.error(f"Failed to get symbol info for {symbol}: {e}")
            return {}
    
    def get_available_symbols(self) -> List[str]:
        """Get list of available symbols"""
        try:
            response = self._make_request('GET', '/api/v1/market/symbols')
            return response.get('symbols', [])
        except Exception as e:
            self.logger.error(f"Failed to get available symbols: {e}")
            return []
    
    def place_order(self, symbol: str, order_type: str, volume: float, price: float = None, 
                   sl: float = None, tp: float = None, comment: str = "", 
                   deviation: int = 10) -> Dict[str, Any]:
        """Place a trading order"""
        try:
            order_data = {
                'symbol': symbol.upper(),
                'type': order_type.upper(),  # "BUY" or "SELL"
                'volume': float(volume),
                'deviation': int(deviation),
                'comment': str(comment)
            }
            
            # Add optional parameters if provided
            if price is not None:
                order_data['price'] = float(price)
            if sl is not None:
                order_data['sl'] = float(sl)
            if tp is not None:
                order_data['tp'] = float(tp)
            
            response = self._make_request('POST', '/api/v1/trade/order', json=order_data)
            return response
        except Exception as e:
            self.logger.error(f"Failed to place order for {symbol}: {e}")
            return {'error': str(e), 'success': False}
    
    def place_market_order(self, symbol: str, order_type: str, volume: float, 
                          sl: float = None, tp: float = None, comment: str = "") -> Dict[str, Any]:
        """Place a market order"""
        return self.place_order(symbol, order_type, volume, sl=sl, tp=tp, comment=comment)
    
    def place_limit_order(self, symbol: str, order_type: str, volume: float, price: float,
                         sl: float = None, tp: float = None, comment: str = "") -> Dict[str, Any]:
        """Place a limit order"""
        return self.place_order(symbol, order_type, volume, price=price, sl=sl, tp=tp, comment=comment)
    
    def place_stop_order(self, symbol: str, order_type: str, volume: float, price: float,
                        sl: float = None, tp: float = None, comment: str = "") -> Dict[str, Any]:
        """Place a stop order"""
        return self.place_order(symbol, order_type, volume, price=price, sl=sl, tp=tp, comment=comment)
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all open positions"""
        try:
            response = self._make_request('GET', '/api/v1/trade/positions')
            return response.get('positions', [])
        except Exception as e:
            self.logger.error(f"Failed to get positions: {e}")
            return []
    
    def get_position_by_ticket(self, ticket: int) -> Dict[str, Any]:
        """Get specific position by ticket number"""
        try:
            response = self._make_request('GET', f'/api/v1/trade/position/{ticket}')
            return response
        except Exception as e:
            self.logger.error(f"Failed to get position {ticket}: {e}")
            return {}
    
    def close_position(self, ticket: int) -> Dict[str, Any]:
        """Close a specific position"""
        try:
            response = self._make_request('DELETE', f'/api/v1/trade/position/{ticket}')
            return response
        except Exception as e:
            self.logger.error(f"Failed to close position {ticket}: {e}")
            return {'error': str(e), 'success': False}
    
    def close_all_positions(self) -> Dict[str, Any]:
        """Close all open positions"""
        try:
            positions = self.get_positions()
            results = []
            
            for position in positions:
                ticket = position.get('ticket')
                if ticket:
                    result = self.close_position(ticket)
                    results.append({'ticket': ticket, 'result': result})
            
            return {'success': True, 'closed_positions': results}
        except Exception as e:
            self.logger.error(f"Failed to close all positions: {e}")
            return {'error': str(e), 'success': False}
    
    def get_orders(self) -> List[Dict[str, Any]]:
        """Get all pending orders"""
        try:
            response = self._make_request('GET', '/api/v1/trade/orders')
            return response.get('orders', [])
        except Exception as e:
            self.logger.error(f"Failed to get orders: {e}")
            return []
    
    def cancel_order(self, ticket: int) -> Dict[str, Any]:
        """Cancel a pending order"""
        try:
            response = self._make_request('DELETE', f'/api/v1/trade/order/{ticket}')
            return response
        except Exception as e:
            self.logger.error(f"Failed to cancel order {ticket}: {e}")
            return {'error': str(e), 'success': False}
    
    def cancel_all_orders(self) -> Dict[str, Any]:
        """Cancel all pending orders"""
        try:
            orders = self.get_orders()
            results = []
            
            for order in orders:
                ticket = order.get('ticket')
                if ticket:
                    result = self.cancel_order(ticket)
                    results.append({'ticket': ticket, 'result': result})
            
            return {'success': True, 'cancelled_orders': results}
        except Exception as e:
            self.logger.error(f"Failed to cancel all orders: {e}")
            return {'error': str(e), 'success': False}
    
    def get_history_deals(self, date_from: str = None, date_to: str = None, 
                         position_id: int = None) -> List[Dict[str, Any]]:
        """Get history of deals"""
        try:
            params = {}
            if date_from:
                params['date_from'] = date_from
            if date_to:
                params['date_to'] = date_to
            if position_id:
                params['position_id'] = position_id
                
            response = self._make_request('GET', '/api/v1/history/deals', params=params)
            return response.get('deals', [])
        except Exception as e:
            self.logger.error(f"Failed to get history deals: {e}")
            return []
    
    def get_history_orders(self, date_from: str = None, date_to: str = None) -> List[Dict[str, Any]]:
        """Get history of orders"""
        try:
            params = {}
            if date_from:
                params['date_from'] = date_from
            if date_to:
                params['date_to'] = date_to
                
            response = self._make_request('GET', '/api/v1/history/orders', params=params)
            return response.get('orders', [])
        except Exception as e:
            self.logger.error(f"Failed to get history orders: {e}")
            return []
    
    def ping(self) -> bool:
        """Ping the API to check connectivity"""
        try:
            response = self._make_request('GET', '/api/v1/ping')
            return response.get('status') == 'ok'
        except Exception:
            return False
