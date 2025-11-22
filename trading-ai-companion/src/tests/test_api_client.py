"""
Test MT5 API Client
"""

import sys
import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import json

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from modules.mt5_connector.api_client import MT5APIClient

class TestMT5APIClient(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.client = MT5APIClient(base_url="http://localhost:8082")
    
    def test_initialization(self):
        """Test API client initialization"""
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.base_url, "http://localhost:8082")
        self.assertIsNotNone(self.client.session)
        print("✓ MT5APIClient initialized successfully")
    
    def test_set_api_key(self):
        """Test API key setting"""
        test_key = "test_api_key_123"
        self.client.set_api_key(test_key)
        
        # Check if header was set
        self.assertEqual(
            self.client.session.headers.get('Authorization'),
            f'Bearer {test_key}'
        )
        print("✓ API key setting working")
    
    @patch('modules.mt5_connector.api_client.requests.Session.request')
    def test_make_request_success(self, mock_request):
        """Test successful request"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'ok', 'data': 'test'}
        mock_response.content = json.dumps({'status': 'ok', 'data': 'test'}).encode()
        mock_request.return_value = mock_response
        
        result = self.client._make_request('GET', '/test')
        
        self.assertEqual(result, {'status': 'ok', 'data': 'test'})
        mock_request.assert_called_once_with('GET', 'http://localhost:8082/test', timeout=30)
        print("✓ Successful request handling working")
    
    @patch('modules.mt5_connector.api_client.requests.Session.request')
    def test_make_request_error(self, mock_request):
        """Test request error handling"""
        # Mock request exception
        mock_request.side_effect = Exception("Connection failed")
        
        with self.assertRaises(Exception) as context:
            self.client._make_request('GET', '/test')
        
        self.assertIn("API request failed", str(context.exception))
        print("✓ Request error handling working")
    
    @patch('modules.mt5_connector.api_client.MT5APIClient._make_request')
    def test_get_server_status(self, mock_make_request):
        """Test server status retrieval"""
        mock_make_request.return_value = {'status': 'connected'}
        
        result = self.client.get_server_status()
        
        self.assertEqual(result, {'status': 'connected'})
        mock_make_request.assert_called_once_with('GET', '/api/v1/status')
        print("✓ Server status retrieval working")
    
    @patch('modules.mt5_connector.api_client.MT5APIClient._make_request')
    def test_get_account_info(self, mock_make_request):
        """Test account info retrieval"""
        mock_account_data = {
            'balance': 10000.0,
            'equity': 10050.0,
            'margin': 1000.0
        }
        mock_make_request.return_value = mock_account_data
        
        result = self.client.get_account_info()
        
        self.assertEqual(result, mock_account_data)
        mock_make_request.assert_called_once_with('GET', '/api/v1/account')
        print("✓ Account info retrieval working")
    
    @patch('modules.mt5_connector.api_client.MT5APIClient._make_request')
    def test_get_market_data(self, mock_make_request):
        """Test market data retrieval"""
        mock_market_data = {
            'symbol': 'EURUSD',
            'bars': [{'time': '2023-01-01', 'open': 1.0500, 'close': 1.0550}]
        }
        mock_make_request.return_value = mock_market_data
        
        result = self.client.get_market_data('EURUSD', 'M1', 100)
        
        self.assertEqual(result, mock_market_data)
        mock_make_request.assert_called_once_with(
            'GET', '/api/v1/market/data',
            params={'symbol': 'EURUSD', 'timeframe': 'M1', 'count': 100}
        )
        print("✓ Market data retrieval working")
    
    @patch('modules.mt5_connector.api_client.MT5APIClient._make_request')
    def test_place_order(self, mock_make_request):
        """Test order placement"""
        mock_response = {'success': True, 'ticket': 12345}
        mock_make_request.return_value = mock_response
        
        result = self.client.place_order('EURUSD', 'BUY', 0.1, comment='Test order')
        
        self.assertEqual(result, mock_response)
        mock_make_request.assert_called_once()
        print("✓ Order placement working")
    
    @patch('modules.mt5_connector.api_client.MT5APIClient._make_request')
    def test_get_positions(self, mock_make_request):
        """Test positions retrieval"""
        mock_positions = {
            'positions': [
                {'ticket': 12345, 'symbol': 'EURUSD', 'type': 'BUY', 'volume': 0.1}
            ]
        }
        mock_make_request.return_value = mock_positions
        
        result = self.client.get_positions()
        
        self.assertEqual(result, mock_positions['positions'])
        mock_make_request.assert_called_once_with('GET', '/api/v1/trade/positions')
        print("✓ Positions retrieval working")

if __name__ == '__main__':
    unittest.main()
