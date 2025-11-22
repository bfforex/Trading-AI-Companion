"""
Web Interface for Trading AI Companion
"""

import logging
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO

class WebInterface:
    def __init__(self, app_instance):
        self.app_instance = app_instance
        self.logger = logging.getLogger(__name__)
        self.flask_app = Flask(__name__)
        self.socketio = SocketIO(self.flask_app)
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        @self.flask_app.route('/')
        def index():
            return render_template('index.html')
        
        @self.flask_app.route('/dashboard')
        def dashboard():
            return render_template('dashboard.html')
        
        @self.flask_app.route('/api/status')
        def api_status():
            return jsonify({
                'status': 'running',
                'mt5_connected': self.app_instance.mt5_manager.is_initialized,
                'models_available': len(self.app_instance.ai_orchestrator.get_available_models())
            })
        
        @self.flask_app.route('/api/models')
        def api_models():
            models = self.app_instance.ai_orchestrator.get_available_models()
            return jsonify(models)
    
    def start(self):
        """Start the web interface"""
        self.logger.info("Starting web interface")
        self.socketio.run(self.flask_app, host='localhost', port=8080, debug=False)
    
    def shutdown(self):
        """Shutdown the web interface"""
        self.logger.info("Shutting down web interface")
        # Flask-SocketIO doesn't have a direct shutdown method
        # The shutdown would be handled by the main application
