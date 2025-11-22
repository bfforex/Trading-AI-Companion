"""
Ollama Provider Implementation
"""

import ollama
import logging
from typing import Dict, Any

class OllamaProvider:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = ollama.Client()
    
    def generate(self, model: str, prompt: str, options: Dict = None) -> Dict[str, Any]:
        """Generate response using Ollama model"""
        try:
            response = self.client.generate(
                model=model,
                prompt=prompt,
                options=options or {}
            )
            return response
        except Exception as e:
            self.logger.error(f"Error generating response with {model}: {e}")
            raise
    
    def chat(self, model: str, messages: list, options: Dict = None) -> Dict[str, Any]:
        """Chat with Ollama model"""
        try:
            response = self.client.chat(
                model=model,
                messages=messages,
                options=options or {}
            )
            return response
        except Exception as e:
            self.logger.error(f"Error in chat with {model}: {e}")
            raise
