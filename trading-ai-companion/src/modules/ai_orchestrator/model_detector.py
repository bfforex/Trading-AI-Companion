"""
Ollama Model Detector
"""

import ollama
import logging
from typing import List, Dict, Optional

class OllamaModelDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = ollama.Client()
        self.available_models = []
        self.model_capabilities = {}
    
    def discover_models(self) -> List[Dict]:
        """Discover all available models in Ollama"""
        try:
            response = self.client.list()
            self.available_models = response.get('models', [])
            self._categorize_models()
            
            self.logger.info(f"Discovered {len(self.available_models)} Ollama models")
            for model in self.available_models:
                self.logger.debug(f"  - {model['name']}")
            
            return self.available_models
        except Exception as e:
            self.logger.error(f"Error discovering Ollama models: {e}")
            return []
    
    def _categorize_models(self):
        """Categorize models based on capabilities"""
        for model in self.available_models:
            model_name = model['name']
            capabilities = self._assess_model_capabilities(model_name)
            self.model_capabilities[model_name] = capabilities
    
    def _assess_model_capabilities(self, model_name: str) -> Dict:
        """Assess what tasks a model is suitable for"""
        capabilities = {
            'general_analysis': True,
            'technical_analysis': False,
            'sentiment_analysis': False,
            'risk_assessment': False,
            'strategy_generation': False,
            'speed_rating': 'medium',  # slow, medium, fast
            'context_length': 2048
        }
        
        # Model-specific capability mapping
        model_name_lower = model_name.lower()
        
        if 'mistral' in model_name_lower:
            capabilities.update({
                'technical_analysis': True,
                'sentiment_analysis': True,
                'speed_rating': 'fast'
            })
        elif 'llama' in model_name_lower:
            capabilities.update({
                'strategy_generation': True,
                'risk_assessment': True,
                'context_length': 4096
            })
        elif 'tiny' in model_name_lower or 'small' in model_name_lower:
            capabilities.update({
                'speed_rating': 'fast',
                'context_length': 1024
            })
        elif 'gemini' in model_name_lower or 'qwen' in model_name_lower:
            capabilities.update({
                'technical_analysis': True,
                'context_length': 32768
            })
        
        return capabilities
    
    def get_models_for_task(self, task_type: str) -> List[str]:
        """Get models suitable for a specific task"""
        suitable_models = []
        
        for model_name, capabilities in self.model_capabilities.items():
            if capabilities.get(task_type, False):
                suitable_models.append(model_name)
        
        # If no specific models found, return all models
        if not suitable_models:
            suitable_models = [model['name'] for model in self.available_models]
        
        return suitable_models
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """Get detailed information about a specific model"""
        for model in self.available_models:
            if model['name'] == model_name:
                return {
                    'name': model['name'],
                    'modified_at': model['modified_at'],
                    'capabilities': self.model_capabilities.get(model_name, {}),
                    'size': model.get('size', 0)
                }
        return None
