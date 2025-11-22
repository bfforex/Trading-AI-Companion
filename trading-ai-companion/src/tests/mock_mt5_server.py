#!/usr/bin/env python3
"""
Mock MT5 REST API Server for Testing
"""

from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

# Mock data
mock_account_info = {
    'balance': 10000.00,
    'equity': 10050.00,
    'margin': 1000.00,
    'free_margin': 9050.00,
    'margin_level': 1005.0,
    'currency': 'USD'
}

mock_positions = [
    {
        'ticket': 123456,
        'symbol': 'EURUSD',
        'type': 'BUY',
        'volume': 0.1,
        'price_open': 1.0520,
        'sl': 1.0480,
        'tp': 1.0600,
        'profit': 50.00
    }
]

@app.route('/api/v1/status')
def get_status():
    return jsonify({
        'status': 'connected',
        'timestamp': time.time(),
        'message': 'Mock MT5 Server Running'
    })

@app.route('/api/v1/account')
def get_account():
    return jsonify(mock_account_info)

@app.route('/api/v1/market/data')
def get_market_data():
    symbol = request.args.get('symbol', 'EURUSD')
    timeframe = request.args.get('timeframe', 'M1')
    count = int(request.args.get('count', 100))
    
    # Generate mock market data
    bars = []
    base_price = 1.0500
    for i in range(count):
        open_price = base_price + random.uniform(-0.01, 0.01)
        high_price = open_price + random.uniform(0, 0.005)
        low_price = open_price - random.uniform(0, 0.005)
        close_price = random.uniform(low_price, high_price)
        
        bars.append({
            'timestamp': time.time() - (count - i) * 60,
            'open': round(open_price, 5),
            'high': round(high_price, 5),
            'low': round(low_price, 5),
            'close': round(close_price, 5),
            'volume': random.randint(100, 1000)
        })
    
    return jsonify({
        'symbol': symbol,
        'timeframe': timeframe,
        'bars': bars
    })

@app.route('/api/v1/trade/positions')
def get_positions():
    return jsonify({
        'positions': mock_positions
    })

@app.route('/api/v1/ping')
def ping():
    return jsonify({
        'status': 'ok',
        'message': 'MT5 REST API is running'
    })

@app.route('/api/v1/trade/order', methods=['POST'])
def place_order():
    order_data = request.json
    return jsonify({
        'success': True,
        'ticket': random.randint(100000, 999999),
        'message': f"Order placed for {order_data.get('symbol', 'UNKNOWN')}"
    })

if __name__ == '__main__':
    print("🚀 Starting Mock MT5 REST API Server...")
    print("   Listening on http://localhost:8082")
    print("   Press Ctrl+C to stop")
    print()
    
    app.run(host='localhost', port=8082, debug=True)
