"""
AI Orchestrator - Manages multiple AI backends
"""

import logging
from typing import Dict, Any, List
from modules.ai_orchestrator.model_detector import OllamaModelDetector
from modules.ai_orchestrator.model_selector import DynamicModelSelector
from modules.ai_orchestrator.performance_monitor import ModelPerformanceMonitor
from modules.ai_orchestrator.providers.ollama_provider import OllamaProvider

class AIOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model_detector = OllamaModelDetector()
        self.model_selector = DynamicModelSelector(self.model_detector)
        self.performance_monitor = ModelPerformanceMonitor()
        self.providers = {}
        
        # Initialize providers
        self._initialize_providers()
        
        # Discover available models
        self.refresh_available_models()
    
    def _initialize_providers(self):
        """Initialize AI providers"""
        try:
            self.providers['ollama'] = OllamaProvider()
            # Add other providers as needed
            # self.providers['gemini'] = GeminiProvider()
            # self.providers['openai'] = OpenAIProvider()
            
            self.logger.info("AI providers initialized")
        except Exception as e:
            self.logger.error(f"Error initializing AI providers: {e}")
    
    def refresh_available_models(self):
        """Refresh the list of available models"""
        self.available_models = self.model_detector.discover_models()
        self.logger.info(f"Found {len(self.available_models)} AI models")
    
    def execute_task(self, task_type: str, prompt: str, priority: str = 'balanced') -> Dict[str, Any]:
        """Execute a task using the best available model"""
        try:
            # Select model for this task
            model_name = self.model_selector.select_model_for_task(task_type, priority)
            
            if not model_name:
                raise Exception("No suitable model available")
            
            self.logger.info(f"Executing {task_type} with model: {model_name}")
            
            # Execute the task using Ollama provider
            if 'ollama' in self.providers:
                start_time = time.time()
                response = self.providers['ollama'].generate(model_name, prompt)
                response_time = time.time() - start_time
                
                # Track performance
                self.performance_monitor.track_model_performance(model_name, response_time)
                
                return {
                    'model': model_name,
                    'response': response,
                    'response_time': response_time,
                    'success': True
                }
            else:
                raise Exception("Ollama provider not available")
                
        except Exception as e:
            self.logger.error(f"Error executing task: {e}")
            return {
                'model': None,
                'response': None,
                'error': str(e),
                'success': False
            }
    
    def get_model_rankings(self, metric: str = 'response_time') -> List[str]:
        """Get models ranked by performance"""
        return self.performance_monitor.get_model_rankings(metric)
    
    def get_available_models(self) -> List[Dict]:
        """Get information about available models"""
        return self.available_models
