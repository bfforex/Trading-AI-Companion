"""
Test MT5 Process Monitor
"""

import sys
import os
import unittest
from pathlib import Path
import time

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from modules.mt5_connector.process_monitor import MT5ProcessMonitor

class TestProcessMonitor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.monitor = MT5ProcessMonitor()
    
    def test_initialization(self):
        """Test monitor initialization"""
        self.assertIsNotNone(self.monitor)
        self.assertIsInstance(self.monitor, MT5ProcessMonitor)
        print("✓ MT5ProcessMonitor initialized successfully")
    
    def test_system_resources(self):
        """Test system resource monitoring"""
        resources = self.monitor.get_system_resources()
        
        self.assertIsInstance(resources, dict)
        self.assertIn('cpu_percent', resources)
        self.assertIn('memory', resources)
        self.assertIn('disk', resources)
        
        # Validate data types
        self.assertIsInstance(resources['cpu_percent'], (int, float))
        self.assertIsInstance(resources['memory'], dict)
        self.assertIsInstance(resources['disk'], dict)
        
        print("✓ System resources monitoring working")
        print(f"  CPU: {resources['cpu_percent']:.1f}%")
        print(f"  Memory: {resources['memory']['percent']:.1f}%")
        print(f"  Disk: {resources['disk']['percent']:.1f}%")
    
    def test_process_detection(self):
        """Test MT5 process detection"""
        processes = self.monitor.find_mt5_processes()
        
        self.assertIsInstance(processes, list)
        print(f"✓ Process detection working - found {len(processes)} MT5 processes")
        
        # Print process information
        for proc in processes:
            print(f"  PID: {proc.get('pid')}, Name: {proc.get('name')}")
    
    def test_process_health_monitoring(self):
        """Test individual process health monitoring"""
        # Get current Python process as test subject
        import psutil
        current_pid = os.getpid()
        
        health = self.monitor.monitor_process_health(current_pid)
        
        self.assertIsInstance(health, dict)
        self.assertEqual(health['pid'], current_pid)
        self.assertIn('status', health)
        self.assertIn('cpu_percent', health)
        self.assertIn('memory_percent', health)
        self.assertTrue(health['running'])
        
        print("✓ Process health monitoring working")
        print(f"  Current process CPU: {health['cpu_percent']:.1f}%")
        print(f"  Current process Memory: {health['memory_percent']:.1f}%")
    
    def test_resource_thresholds(self):
        """Test resource threshold checking"""
        # Test with very high thresholds to avoid alerts
        thresholds = {
            'cpu_percent': 100.0,
            'memory_percent': 100.0,
            'disk_percent': 100.0
        }
        
        result = self.monitor.check_resource_thresholds(thresholds)
        
        self.assertIsInstance(result, dict)
        self.assertIn('system_resources', result)
        self.assertIn('alerts', result)
        self.assertIn('status', result)
        
        print("✓ Resource threshold checking working")
        print(f"  Status: {result['status']}")
        print(f"  Alerts: {len(result['alerts'])}")

if __name__ == '__main__':
    unittest.main()
