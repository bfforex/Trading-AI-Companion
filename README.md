# Trading AI Companion App

An intelligent trading assistant that leverages multiple AI backends including Ollama, Google Gemini Nano, OpenAI, and Claude to provide comprehensive support for human traders.

## Features

### AI Capabilities
- **Multi-AI Backend Support**: Seamlessly integrates Ollama, Gemini Nano, OpenAI, Claude, and Hugging Face models
- **Automatic Model Discovery**: Detects all available local models in Ollama
- **Dynamic Model Selection**: Chooses the best model for each task based on capabilities
- **Performance Monitoring**: Tracks model performance and adapts accordingly
- **Hybrid Decision Making**: Combines insights from multiple AI sources

### Trading Features
- **MT5 Integration**: Auto-launches MT5 and REST API server
- **Real-time Market Analysis**: Technical and fundamental analysis
- **Risk Management**: Position sizing, stop-losses, portfolio risk monitoring
- **Sentiment Analysis**: News and social media sentiment processing
- **Strategy Development**: AI-assisted strategy creation and optimization

### System Features
- **Modular Architecture**: Independent, testable modules
- **Web-based UI**: Responsive dashboard for monitoring and control
- **CLI Interface**: Command-line access for advanced users
- **Configuration Management**: Flexible YAML-based configuration
- **Comprehensive Logging**: Detailed activity and error logging

## Requirements

- Python 3.8+
- Ollama (with desired models installed)
- MetaTrader 5
- Windows/Linux/macOS

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/trading-ai-companion.git
   cd trading-ai-companion
