"""
Core Application Orchestrator
"""

import logging
from typing import Dict, Any

class CoreOrchestrator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.components = {}
    
    def register_component(self, name: str, component: Any):
        """Register a component with the orchestrator"""
        self.components[name] = component
        self.logger.info(f"Component {name} registered")
    
    def get_component(self, name: str) -> Any:
        """Get a registered component"""
        return self.components.get(name)
    
    def initialize_all(self) -> bool:
        """Initialize all components"""
        try:
            for name, component in self.components.items():
                if hasattr(component, 'initialize'):
                    component.initialize()
            return True
        except Exception as e:
            self.logger.error(f"Error initializing components: {e}")
            return False
