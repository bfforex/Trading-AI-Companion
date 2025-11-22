#!/usr/bin/env python3
"""
Script to install recommended Ollama models for trading
"""

import subprocess
import sys

def install_models():
    """Install recommended models for trading tasks"""
    models = [
        "mistral",      # General purpose, good for technical analysis
        "llama2",       # Strategy generation and risk assessment
        "tinyllama",    # Fast responses for quick insights
        "neural-chat",  # Conversation and explanation tasks
    ]
    
    print("Installing recommended Ollama models for trading...")
    
    for model in models:
        print(f"Installing {model}...")
        try:
            result = subprocess.run(["ollama", "pull", model], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print(f"✓ {model} installed successfully")
            else:
                print(f"✗ Failed to install {model}: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"✗ Timeout installing {model}")
        except Exception as e:
            print(f"✗ Error installing {model}: {e}")
    
    print("Model installation complete!")

if __name__ == "__main__":
    install_models()
