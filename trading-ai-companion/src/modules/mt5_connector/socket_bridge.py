"""
MT5 Socket Bridge - Named Pipes/Unix Sockets for High-Performance Communication
"""

import os
import json
import time
import logging
import threading
import platform
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
import socket

class MT5SocketBridge:
    def __init__(self, socket_path: str = None):
        self.logger = logging.getLogger(__name__)
        self.socket_path = socket_path or self._get_default_socket_path()
        self.is_server = False
        self.socket = None
        self.client_socket = None
        self.is_connected = False
        
    def _get_default_socket_path(self) -> str:
        """Get default socket path based on OS"""
        system = platform.system()
        
        if system == "Windows":
            # Use named pipes on Windows
            return r"\\.\pipe\TradingAI_MT5_Bridge"
        elif system == "Darwin":  # macOS
            return "/tmp/tradingai_mt5_bridge.sock"
        else:  # Linux
            return "/tmp/tradingai_mt5_bridge.sock"
    
    def start_server(self):
        """Start socket server for MT5 to connect to"""
        try:
            system = platform.system()
            
            if system == "Windows":
                # Windows named pipes require pywin32
                import win32pipe, win32file
                self.pipe = win32pipe.CreateNamedPipe(
                    self.socket_path,
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
                    1, 65536, 65536, 0, None
                )
                self.is_server = True
                self.logger.info(f"Named pipe server started: {self.socket_path}")
            else:
                # Unix domain socket
                if os.path.exists(self.socket_path):
                    os.unlink(self.socket_path)
                
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.socket.bind(self.socket_path)
                self.socket.listen(1)
                self.is_server = True
                self.logger.info(f"Unix socket server started: {self.socket_path}")
                
        except Exception as e:
            self.logger.error(f"Failed to start socket server: {e}")
            raise
    
    def connect_client(self):
        """Connect as client to MT5 socket server"""
        try:
            system = platform.system()
            
            if system == "Windows":
                # Connect to named pipe
                import win32file
                self.handle = win32file.CreateFile(
                    self.socket_path,
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0, None,
                    win32file.OPEN_EXISTING,
                    0, None
                )
                self.is_connected = True
                self.logger.info("Connected to MT5 named pipe")
            else:
                # Connect to Unix socket
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.socket.connect(self.socket_path)
                self.is_connected = True
                self.logger.info("Connected to MT5 Unix socket")
                
        except Exception as e:
            self.logger.error(f"Failed to connect to socket: {e}")
            raise
    
    def send_message(self, message: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
        """Send message and wait for response"""
        try:
            message_str = json.dumps(message)
            
            if platform.system() == "Windows":
                import win32file
                # Send message length first
                message_bytes = message_str.encode('utf-8')
                win32file.WriteFile(self.handle, f"{len(message_bytes)}\n".encode('utf-8'))
                win32file.WriteFile(self.handle, message_bytes)
                
                # Read response length
                result, length_data = win32file.ReadFile(self.handle, 1024)
                length = int(length_data.decode('utf-8').strip())
                
                # Read response
                result, response_data = win32file.ReadFile(self.handle, length)
                response_str = response_data.decode('utf-8')
                return json.loads(response_str)
            else:
                # Send message length first
                message_bytes = message_str.encode('utf-8')
                self.socket.send(f"{len(message_bytes)}\n".encode('utf-8'))
                self.socket.send(message_bytes)
                
                # Read response length
                length_line = self.socket.recv(1024).decode('utf-8').strip()
                length = int(length_line)
                
                # Read response
                response_data = self.socket.recv(length)
                response_str = response_data.decode('utf-8')
                return json.loads(response_str)
                
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return {'error': str(e), 'success': False}
    
    def listen_for_connections(self, handler_func):
        """Listen for incoming connections (server mode)"""
        try:
            if platform.system() == "Windows":
                import win32pipe
                while True:
                    win32pipe.ConnectNamedPipe(self.pipe, None)
                    self._handle_client_connection(handler_func)
                    win32pipe.DisconnectNamedPipe(self.pipe)
            else:
                while True:
                    self.client_socket, client_address = self.socket.accept()
                    self._handle_client_connection(handler_func)
                    self.client_socket.close()
        except Exception as e:
            self.logger.error(f"Error listening for connections: {e}")
    
    def _handle_client_connection(self, handler_func):
        """Handle individual client connection"""
        try:
            while True:
                if platform.system() == "Windows":
                    import win32file
                    # Read message length
                    result, length_data = win32file.ReadFile(self.pipe, 1024)
                    length = int(length_data.decode('utf-8').strip())
                    
                    # Read message
                    result, message_data = win32file.ReadFile(self.pipe, length)
                    message_str = message_data.decode('utf-8')
                else:
                    # Read message length
                    length_line = self.client_socket.recv(1024).decode('utf-8').strip()
                    if not length_line:
                        break
                    length = int(length_line)
                    
                    # Read message
                    message_data = self.client_socket.recv(length)
                    message_str = message_data.decode('utf-8')
                
                message = json.loads(message_str)
                response = handler_func(message)
                
                # Send response
                response_str = json.dumps(response)
                if platform.system() == "Windows":
                    import win32file
                    response_bytes = response_str.encode('utf-8')
                    win32file.WriteFile(self.pipe, f"{len(response_bytes)}\n".encode('utf-8'))
                    win32file.WriteFile(self.pipe, response_bytes)
                else:
                    response_bytes = response_str.encode('utf-8')
                    self.client_socket.send(f"{len(response_bytes)}\n".encode('utf-8'))
                    self.client_socket.send(response_bytes)
                    
        except Exception as e:
            self.logger.error(f"Error handling client connection: {e}")
    
    def close(self):
        """Close socket connections"""
        try:
            if platform.system() == "Windows":
                if hasattr(self, 'handle'):
                    import win32file
                    win32file.CloseHandle(self.handle)
                if hasattr(self, 'pipe'):
                    import win32file
                    win32file.CloseHandle(self.pipe)
            else:
                if self.client_socket:
                    self.client_socket.close()
                if self.socket:
                    self.socket.close()
                if os.path.exists(self.socket_path) and not self.is_server:
                    os.unlink(self.socket_path)
        except Exception as e:
            self.logger.error(f"Error closing socket: {e}")
