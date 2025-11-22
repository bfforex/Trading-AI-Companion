#!/usr/bin/env python3
"""
Comprehensive Test Runner for Phase 1
"""

import sys
import os
import unittest
from pathlib import Path
import time

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

def run_tests():
    """Run all Phase 1 tests"""
    print("=" * 60)
    print("Trading AI Companion - Phase 1 Test Suite")
    print("=" * 60)
    print()
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Test modules to run
    test_modules = [
        'src.tests.test_setup',
        'src.tests.test_process_monitor', 
        'src.tests.test_mt5_manager',
        'src.tests.test_api_client',
        'src.tests.test_integration',
        'src.tests.test_cli'
    ]
    
    # Run tests
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    start_time = time.time()
    
    for module_name in test_modules:
        print(f"\nRunning tests for: {module_name}")
        print("-" * 40)
        
        try:
            # Load and run test suite
            suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
            runner = unittest.TextTestRunner(verbosity=0)
            result = runner.run(suite)
            
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)
            
            # Print individual test results
            for test, traceback in result.failures:
                print(f"FAIL: {test}")
                print(traceback)
                print()
            
            for test, traceback in result.errors:
                print(f"ERROR: {test}")
                print(traceback)
                print()
                
        except Exception as e:
            print(f"Error running {module_name}: {e}")
            total_errors += 1
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests run: {total_tests}")
    print(f"Failures: {total_failures}")
    print(f"Errors: {total_errors}")
    print(f"Success rate: {((total_tests - total_failures - total_errors) / total_tests * 100):.1f}%" if total_tests > 0 else "0%")
    print(f"Duration: {duration:.2f} seconds")
    
    if total_failures == 0 and total_errors == 0:
        print("\n🎉 ALL TESTS PASSED! Phase 1 is working correctly.")
        return True
    else:
        print(f"\n❌ {total_failures + total_errors} issues found. Please review the failures above.")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
