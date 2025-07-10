# Installation & Setup

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### Recommended Specifications
- **Python**: 3.9 or 3.10
- **RAM**: 8GB or more
- **Storage**: 5GB free space (for models and data)
- **Internet**: Stable connection for API calls

## 🔧 Installation Methods

### Method 1: Standard Installation (Recommended)

#### 1. Install Python
**Windows:**
```bash
# Download from python.org or use Windows Store
# Or install via chocolatey
choco install python
```

**macOS:**
```bash
# Install via Homebrew
brew install python@3.9
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.9 python3.9-pip python3.9-venv
```

#### 2. Clone Repository
```bash
git clone https://github.com/your-org/aara-health-agent.git
cd aara-health-agent
```

#### 3. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Method 2: Docker Installation

#### Prerequisites
- Docker Desktop installed
- Docker Compose (included with Docker Desktop)

#### Steps
```bash
# Clone repository
git clone https://github.com/your-org/aara-health-agent.git
cd aara-health-agent

# Build and run with Docker Compose
docker-compose up --build
```

### Method 3: Development Installation

For contributors and developers:

```bash
# Clone repository
git clone https://github.com/your-org/aara-health-agent.git
cd aara-health-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## 🔑 API Keys Setup

### Required API Keys

#### 1. OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account or sign in
3. Navigate to API Keys section
4. Create new secret key
5. Copy key for environment setup

#### 2. Tavily API Key
1. Visit [Tavily AI](https://tavily.com/)
2. Sign up for account
3. Navigate to dashboard
4. Generate API key
5. Copy key for environment setup

### Environment Configuration

#### Create .env File
```bash
# Copy example file
cp .env.example .env

# Edit with your favorite editor
nano .env  # or code .env, vim .env, etc.
```

#### .env File Content
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

# Tavily Search Configuration
TAVILY_API_KEY=your_tavily_api_key_here
TAVILY_MAX_RESULTS=5

# Agent Configuration
AGENT_NAME=Ara
AGENT_DESCRIPTION=Your AI companion for women's health and skincare
AGENT_PERSONALITY=empathetic
AGENT_RESPONSE_STYLE=supportive

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/ara.log
LOG_MAX_SIZE=10485760  # 10MB
LOG_BACKUP_COUNT=5

# Database Configuration
VECTOR_DB_PATH=data/vectorstore
VECTOR_DB_COLLECTION=ara_knowledge

# Safety Configuration
ENABLE_SAFETY_CHECKS=true
ENABLE_EMERGENCY_DETECTION=true
ENABLE_CRISIS_INTERVENTION=true

# Performance Configuration
ENABLE_CACHING=true
CACHE_TTL=3600  # 1 hour
MAX_CONCURRENT_REQUESTS=10
```

## 📦 Dependencies Installation

### Core Dependencies
```bash
# Core AI and workflow libraries
langchain==0.1.0
langgraph==0.0.20
openai==1.3.0

# Search and knowledge base
tavily-python==0.3.0
chromadb==0.4.0

# Data processing
pydantic==2.5.0
pyyaml==6.0
python-dotenv==1.0.0

# Utilities
requests==2.31.0
numpy==1.24.0
pandas==2.0.0
```

### Development Dependencies
```bash
# Testing
pytest==7.4.0
pytest-asyncio==0.21.0
pytest-cov==4.1.0

# Code quality
black==23.0.0
flake8==6.0.0
mypy==1.5.0
pre-commit==3.4.0

# Documentation
mkdocs==1.5.0
mkdocs-material==9.2.0
```

## 🗄️ Database Setup

### Initialize Vector Database
```bash
# Run setup script
python scripts/setup_vectorstore.py

# Verify setup
python -c "from scripts.setup_vectorstore import verify_setup; verify_setup()"
```

### Manual Database Setup
```python
# If automatic setup fails
from chromadb import Client
from chromadb.config import Settings

# Create client
client = Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="data/vectorstore"
))

# Create collection
collection = client.create_collection(
    name="ara_knowledge",
    metadata={"description": "Ara health and skincare knowledge base"}
)

print("Database setup complete!")
```

## 🧪 Verify Installation

### Quick Test
```bash
# Run basic functionality test
python quick_test.py
```

### Comprehensive Test
```bash
# Run full test suite
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_rules.py -v
python -m pytest tests/test_tools.py -v
python -m pytest tests/test_workflow.py -v
```

### Manual Verification
```bash
# Test individual components
python test_simple.py
python test_expanded_rules.py
python test_greetings.py
```

## 🚀 First Run

### Start the Agent
```bash
# Basic startup
python scripts/run_agent.py

# With debug logging
python scripts/run_agent.py --debug

# With custom configuration
python scripts/run_agent.py --config custom_config.yaml
```

### Expected Output
```
🌸 Ara Health Agent Starting...
✅ Configuration loaded
✅ Rules engine initialized
✅ Vector database connected
✅ Tools loaded successfully
✅ Safety systems active

🌸 Ara Health Agent Started
Type 'quit' to exit, 'help' for commands

You: 
```

## 🔧 Troubleshooting Installation

### Common Issues

#### Python Version Issues
```bash
# Check Python version
python --version

# If version is too old, install newer version
# Windows: Download from python.org
# macOS: brew install python@3.9
# Linux: sudo apt install python3.9
```

#### Virtual Environment Issues
```bash
# If venv creation fails
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv
```

#### Dependency Installation Errors
```bash
# Clear pip cache
pip cache purge

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install with no cache
pip install --no-cache-dir -r requirements.txt
```

#### API Key Issues
```bash
# Verify .env file exists
ls -la .env

# Check environment variables
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

#### Database Connection Issues
```bash
# Check database directory
ls -la data/vectorstore/

# Recreate database
rm -rf data/vectorstore/
python scripts/setup_vectorstore.py
```

#### UTF-8 Encoding Issues (Windows)
```bash
# Set environment variable
set PYTHONIOENCODING=utf-8

# Or in PowerShell
$env:PYTHONIOENCODING="utf-8"
```

### Platform-Specific Issues

#### Windows Issues
```bash
# Long path support
git config --global core.longpaths true

# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS Issues
```bash
# Xcode command line tools
xcode-select --install

# Certificate issues
/Applications/Python\ 3.9/Install\ Certificates.command
```

#### Linux Issues
```bash
# Missing system dependencies
sudo apt install build-essential python3-dev

# Permission issues
sudo chown -R $USER:$USER ~/.local/
```

## 📊 Performance Optimization

### Memory Optimization
```bash
# Set memory limits
export PYTHONMALLOC=malloc
export MALLOC_ARENA_MAX=2
```

### CPU Optimization
```bash
# Set number of workers
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
```

### Disk Space Management
```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# Clear pip cache
pip cache purge
```

## 🔄 Updates and Maintenance

### Update Installation
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Update database
python scripts/setup_vectorstore.py --update
```

### Backup Configuration
```bash
# Backup important files
cp .env .env.backup
cp -r data/vectorstore/ data/vectorstore.backup/
```

## 🆘 Getting Help

### Documentation
- [Quick Start Guide](quick-start.md)
- [Configuration Guide](configuration.md)
- [Troubleshooting Guide](../troubleshooting/common-issues.md)

### Community Support
- **GitHub Issues**: [Report bugs](https://github.com/your-org/aara-health-agent/issues)
- **Discussions**: [Community forum](https://github.com/your-org/aara-health-agent/discussions)
- **Email**: support@hermirror.com

### Professional Support
- **Enterprise Support**: enterprise@hermirror.com
- **Custom Development**: dev@hermirror.com

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] API keys configured in .env file
- [ ] Vector database initialized
- [ ] Tests passing
- [ ] Agent starts without errors
- [ ] Basic conversation test successful

Congratulations! You now have Ara Health Agent installed and ready to use. 🎉 