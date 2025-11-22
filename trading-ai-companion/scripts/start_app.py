#!/usr/bin/env python3
"""
Convenience script to start the Trading AI Companion
"""

import subprocess
import sys
import os

def start_app():
    """Start the main application"""
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_dir)
        
        # Start the application
        subprocess.run([sys.executable, "src/main.py"] + sys.argv[1:])
        
    except KeyboardInterrupt:
        print("Application stopped by user")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    start_app()
