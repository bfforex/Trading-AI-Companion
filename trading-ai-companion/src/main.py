#!/usr/bin/env python3
"""
Main entry point for the Trading AI Companion App - Updated with MT5 Integration
"""

import argparse
import sys
import os
import json
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.core.app import TradingAIApp
from src.utils.logger import setup_logger

def main():
    parser = argparse.ArgumentParser(description="Trading AI Companion App")
    parser.add_argument("--config", help="path to configuration file")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--status", action="store_true", help="Show system status and exit")
    parser.add_argument("--test-order", nargs=3, metavar=('SYMBOL', 'TYPE', 'VOLUME'), 
                       help="Place a test order (symbol type volume)")
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = "logs/app.log"
    logger = setup_logger("TradingAI", log_file, level="DEBUG" if args.debug else "INFO")
    logger.info("Starting Trading AI Companion App")
    
    try:
        # Initialize the application
        app = TradingAIApp(config_path=args.config, debug=args.debug)
        
        # Handle status check
        if args.status:
            if app.start_core_services():
                status = app.get_system_status()
                print(json.dumps(status, indent=2))
            else:
                print("Failed to initialize services")
                sys.exit(1)
            return
        
        # Handle test order
        if args.test_order:
            if app.start_core_services():
                symbol, order_type, volume = args.test_order
                result = app.place_test_order(symbol, order_type, float(volume))
                print(json.dumps(result, indent=2))
            else:
                print("Failed to initialize services")
                sys.exit(1)
            return
        
        # Start core services
        if not app.start_core_services():
            logger.error("Failed to start core services")
            sys.exit(1)
        
        # Start the application
        if args.cli:
            start_cli_interface(app, logger)
        else:
            start_web_interface(app, logger)
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        if 'app' in locals():
            app.shutdown()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}")
        if 'app' in locals():
            app.shutdown()
        sys.exit(1)

def start_cli_interface(app, logger):
    """Start the CLI interface"""
    logger.info("Starting CLI interface")
    print("Trading AI Companion CLI")
    print("Type 'help' for available commands")
    
    while app.is_running:
        try:
            command = input("> ").strip().lower()
            
            if command == "quit" or command == "exit":
                break
            elif command == "help":
                print_help()
            elif command == "status":
                status = app.get_system_status()
                print(json.dumps(status, indent=2))
            elif command == "account":
                summary = app.get_account_summary()
                print(json.dumps(summary, indent=2))
            elif command.startswith("order "):
                # Simple order placement: order EURUSD BUY 0.1
                parts = command.split()
                if len(parts) == 4:
                    symbol, order_type, volume = parts[1], parts[2], parts[3]
                    result = app.place_test_order(symbol, order_type, float(volume))
                    print(json.dumps(result, indent=2))
                else:
                    print("Usage: order SYMBOL TYPE VOLUME")
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            logger.error(f"CLI error: {e}")
            print(f"Error: {e}")
    
    app.shutdown()

def start_web_interface(app, logger):
    """Placeholder for web interface"""
    logger.info("Web interface would start here")
    print("Web interface would start on http://localhost:8080")
    print("Press Ctrl+C to stop")
    
    try:
        # Simple loop to keep app running
        while app.is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    app.shutdown()

def print_help():
    """Print CLI help"""
    help_text = """
Available commands:
  help          - Show this help
  status        - Show system status
  account       - Show account summary
  order SYMBOL TYPE VOLUME  - Place a test order
  quit/exit     - Exit the application
    """
    print(help_text)

if __name__ == "__main__":
    main()
