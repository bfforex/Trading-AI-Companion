"""
Dynamic Model Selector
"""

import logging
from typing import List, Dict
from modules.ai_orchestrator.model_detector import OllamaModelDetector

class DynamicModelSelector:
    def __init__(self, model_detector: OllamaModelDetector):
        self.detector = model_detector
        self.logger = logging.getLogger(__name__)
        self.task_model_mapping = self._initialize_task_mapping()
    
    def _initialize_task_mapping(self) -> Dict:
        """Initialize default task-to-model mapping"""
        return {
            'technical_analysis': ['mistral', 'llama'],
            'sentiment_analysis': ['mistral', 'tiny'],
            'risk_assessment': ['llama', 'mistral'],
            'strategy_generation': ['llama', 'mistral'],
            'quick_insights': ['tiny', 'mistral']
        }
    
    def select_model_for_task(self, task_type: str, priority: str = 'balanced') -> str:
        """Select the best available model for a specific task"""
        # Get candidate models for this task
        candidates = self.task_model_mapping.get(task_type, ['mistral'])
        
        # Find available models that match candidates
        available_candidates = [
            model for model in self.detector.available_models 
            if any(candidate in model['name'] for candidate in candidates)
        ]
        
        if not available_candidates:
            # Fallback to any available model
            return self.detector.available_models[0]['name'] if self.detector.available_models else None
        
        # Select based on priority
        if priority == 'speed':
            return self._select_fastest_model(available_candidates)
        elif priority == 'quality':
            return self._select_highest_quality_model(available_candidates)
        else:  # balanced
            return self._select_balanced_model(available_candidates)
    
    def _select_fastest_model(self, candidates: List) -> str:
        """Select the fastest model based on capabilities"""
        # Prefer models tagged as fast
        fast_models = [
            m for m in candidates 
            if self.detector.model_capabilities.get(m['name'], {}).get('speed_rating') == 'fast'
        ]
        return fast_models[0]['name'] if fast_models else candidates[0]['name']
    
    def _select_highest_quality_model(self, candidates: List) -> str:
        """Select model with highest context length (proxy for quality)"""
        return max(candidates, key=lambda x: 
                  self.detector.model_capabilities.get(x['name'], {}).get('context_length', 0))['name']
    
    def _select_balanced_model(self, candidates: List) -> str:
        """Select a balanced model"""
        # Prefer models that are neither too slow nor too resource-intensive
        balanced_models = [
            m for m in candidates 
            if self.detector.model_capabilities.get(m['name'], {}).get('speed_rating') in ['fast', 'medium']
        ]
        return balanced_models[0]['name'] if balanced_models else candidates[0]['name']
