"""
Test AI Orchestrator
"""

import unittest
from unittest.mock import Mock, patch
from modules.ai_orchestrator.orchestrator import AIOrchestrator

class TestAIOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = AIOrchestrator()
    
    def test_initialize_orchestrator(self):
        """Test orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator)
        self.assertTrue(hasattr(self.orchestrator, 'model_detector'))
    
    @patch('modules.ai_orchestrator.model_detector.OllamaModelDetector.discover_models')
    def test_model_discovery(self, mock_discover):
        """Test model discovery"""
        mock_discover.return_value = [
            {'name': 'mistral', 'modified_at': '2023-01-01'}
        ]
        
        models = self.orchestrator.refresh_available_models()
        self.assertEqual(len(models), 1)
        self.assertEqual(models[0]['name'], 'mistral')

if __name__ == '__main__':
    unittest.main()
