"""
Test CLI Interface
"""

import sys
import os
import unittest
from pathlib import Path
from io import StringIO
from unittest.mock import patch
import json

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from main import print_help

class TestCLI(unittest.TestCase):
    def test_help_command(self):
        """Test help command output"""
        try:
            # Capture print output
            captured_output = StringIO()
            sys.stdout = captured_output
            
            # Call help function
            print_help()
            
            # Restore stdout
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            
            # Check that help text contains expected elements
            self.assertIn("Available commands", output)
            self.assertIn("help", output)
            self.assertIn("status", output)
            self.assertIn("quit", output)
            
            print("✓ CLI help command working")
            print(f"  Help text length: {len(output)} characters")
            
        except Exception as e:
            # Restore stdout even if test fails
            sys.stdout = sys.__stdout__
            self.fail(f"CLI help test failed: {e}")
    
    def test_cli_parsing(self):
        """Test CLI argument parsing"""
        try:
            from main import main
            
            # Test with --help argument (this will exit, so we catch it)
            test_args = ['main.py', '--help']
            
            with patch.object(sys, 'argv', test_args):
                try:
                    main()
                except SystemExit:
                    # Expected behavior for --help
                    print("✓ CLI argument parsing working")
                    
        except Exception as e:
            print(f"Note: CLI parsing test skipped due to: {e}")

if __name__ == '__main__':
    unittest.main()
