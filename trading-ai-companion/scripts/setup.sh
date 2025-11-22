
### scripts/setup.sh
```bash
#!/bin/bash
# Setup script for Trading AI Companion

echo "Setting up Trading AI Companion..."

# Create necessary directories
echo "Creating directory structure..."
mkdir -p config src/{core,modules/{ai_orchestrator/providers,mt5_connector,risk_manager,data_processor,ui/{web_interface/{templates,static/{css,js}},cli_interface},utils,tests} scripts docs logs data models

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install recommended Ollama models
echo "Installing recommended Ollama models..."
python scripts/install_models.py

# Create log directory
echo "Setting up logging..."
mkdir -p logs

# Display completion message
echo "Setup complete!"
echo "Next steps:"
echo "1. Configure the application in config/config.yaml"
echo "2. Start the application: python src/main.py"
echo "3. Access the web interface at http://localhost:8080"
