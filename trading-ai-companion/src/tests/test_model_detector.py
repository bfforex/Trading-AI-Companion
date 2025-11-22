"""
Test Model Detector
"""

import unittest
from unittest.mock import Mock, patch
from modules.ai_orchestrator.model_detector import OllamaModelDetector

class TestModelDetector(unittest.TestCase):
    def setUp(self):
        self.detector = OllamaModelDetector()
    
    def test_initialize_detector(self):
        """Test detector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertTrue(hasattr(self.detector, 'client'))
    
    def test_assess_model_capabilities(self):
        """Test model capability assessment"""
        capabilities = self.detector._assess_model_capabilities('mistral')
        self.assertTrue(capabilities['general_analysis'])
        
        capabilities = self.detector._assess_model_capabilities('tinyllama')
        self.assertEqual(capabilities['speed_rating'], 'fast')

if __name__ == '__main__':
    unittest.main()
