#!/bin/bash

# Ara Health Agent - Quick Setup Script
echo "🌸 Ara Health Agent - Quick Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+ first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Setup Python backend
echo "🔧 Setting up Python backend..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# Tavily Search Configuration
TAVILY_API_KEY=your_tavily_api_key_here

# Agent Configuration
AGENT_NAME=Ara
AGENT_DESCRIPTION=Your AI companion for women's health and skincare

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/ara.log
EOF
    echo -e "${YELLOW}⚠️  Please update the .env file with your actual API keys!${NC}"
fi

# Setup vector store
echo "🗂️  Setting up vector store..."
python scripts/setup_vectorstore.py

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "🚀 Quick Start:"
echo "1. Update your .env file with actual API keys"
echo "2. Start the backend: python scripts/run_api.py"
echo "3. Start the frontend: cd frontend && npm run dev"
echo "4. Open http://localhost:3000"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo "🌸 Happy coding with Ara!" 