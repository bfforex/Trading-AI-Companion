"""
Base AI Provider Interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response from the AI model"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the provider's model"""
        pass
