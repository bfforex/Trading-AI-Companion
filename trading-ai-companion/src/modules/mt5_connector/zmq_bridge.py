"""
MT5 ZeroMQ Bridge - Professional High-Performance Communication
"""

import zmq
import json
import logging
import threading
from typing import Dict, Any, Callable
from datetime import datetime

class MT5ZMQBridge:
    def __init__(self, port: int = 5555, host: str = "localhost"):
        self.logger = logging.getLogger(__name__)
        self.port = port
        self.host = host
        self.context = zmq.Context()
        self.socket = None
        self.is_server = False
        
    def start_server(self):
        """Start ZMQ server for MT5 to connect to"""
        try:
            self.socket = self.context.socket(zmq.REP)  # Reply socket
            self.socket.bind(f"tcp://{self.host}:{self.port}")
            self.is_server = True
            self.logger.info(f"ZMQ server started on tcp://{self.host}:{self.port}")
        except Exception as e:
            self.logger.error(f"Failed to start ZMQ server: {e}")
            raise
    
    def connect_client(self):
        """Connect as client to MT5 ZMQ server"""
        try:
            self.socket = self.context.socket(zmq.REQ)  # Request socket
            self.socket.connect(f"tcp://{self.host}:{self.port}")
            self.logger.info(f"Connected to MT5 ZMQ server at tcp://{self.host}:{self.port}")
        except Exception as e:
            self.logger.error(f"Failed to connect to ZMQ server: {e}")
            raise
    
    def send_request(self, command: str, data: Dict[str, Any] = None, timeout: int = 30000) -> Dict[str, Any]:
        """Send request and wait for response"""
        try:
            request = {
                'command': command,
                'data': data or {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Send request
            message = json.dumps(request)
            self.socket.send_string(message)
            
            # Set timeout
            if timeout:
                poller = zmq.Poller()
                poller.register(self.socket, zmq.POLLIN)
                if poller.poll(timeout):
                    response = self.socket.recv_string()
                    return json.loads(response)
                else:
                    raise TimeoutError("Request timeout")
            else:
                response = self.socket.recv_string()
                return json.loads(response)
                
        except Exception as e:
            self.logger.error(f"Error sending request: {e}")
            return {'error': str(e), 'success': False}
    
    def start_message_loop(self, handler_func: Callable[[Dict], Dict]):
        """Start message processing loop (server mode)"""
        try:
            while True:
                # Wait for request
                message = self.socket.recv_string()
                request = json.loads(message)
                
                # Process request
                response = handler_func(request)
                
                # Send response
                response_message = json.dumps(response)
                self.socket.send_string(response_message)
                
        except Exception as e:
            self.logger.error(f"Error in message loop: {e}")
    
    def close(self):
        """Close ZMQ connections"""
        try:
            if self.socket:
                self.socket.close()
            if self.context:
                self.context.term()
        except Exception as e:
            self.logger.error(f"Error closing ZMQ: {e}")
