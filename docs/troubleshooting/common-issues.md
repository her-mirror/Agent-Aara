# Common Issues & Solutions

## 🔧 Overview

This guide covers the most common issues users encounter with the Aara Health Agent and provides step-by-step solutions to resolve them.

## 🚨 Installation Issues

### Python Version Problems

#### Issue: "Python version not supported"
```
ERROR: This package requires Python 3.8 or higher
```

**Solution:**
```bash
# Check current Python version
python --version

# Install correct Python version
# Windows (via Microsoft Store or python.org)
# macOS
brew install python@3.9
# Linux
sudo apt install python3.9 python3.9-pip python3.9-venv
```

#### Issue: "python command not found"
```
'python' is not recognized as an internal or external command
```

**Solutions:**
1. **Windows**: Add Python to PATH or use `py` command
2. **macOS/Linux**: Use `python3` instead of `python`
3. **Alternative**: Create alias in shell profile

### Virtual Environment Issues

#### Issue: Virtual environment creation fails
```
ERROR: Could not create virtual environment
```

**Solution:**
```bash
# Install virtualenv if missing
pip install virtualenv

# Create virtual environment with full path
python -m venv /full/path/to/venv

# Alternative: Use conda
conda create -n Aara-env python=3.9
conda activate Aara-env
```

#### Issue: "venv\Scripts\activate not found"
```
The system cannot find the path specified
```

**Solution:**
```bash
# Windows - Check Scripts directory
dir venv\Scripts\

# If missing, recreate virtual environment
rmdir /s venv
python -m venv venv

# Alternative activation methods
# PowerShell
venv\Scripts\Activate.ps1
# Command Prompt
venv\Scripts\activate.bat
```

### Dependency Installation Problems

#### Issue: "pip install fails with permission error"
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or ensure virtual environment is activated
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Then install
pip install -r requirements.txt
```

#### Issue: "No module named 'langchain'"
```
ModuleNotFoundError: No module named 'langchain'
```

**Solution:**
```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Reinstall requirements
pip install --upgrade pip
pip install -r requirements.txt

# Check installation
pip list | grep langchain
```

## 🔑 API Key Issues

### OpenAI API Key Problems

#### Issue: "OpenAI API key not found"
```
ERROR: OpenAI API key not found in environment variables
```

**Solution:**
```bash
# Check if .env file exists
ls -la .env

# Create .env file if missing
cp .env.example .env

# Edit .env file and add your key
OPENAI_API_KEY=your_actual_api_key_here

# Verify environment variable
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

#### Issue: "Invalid API key"
```
ERROR: Invalid API key provided
```

**Solutions:**
1. **Check key format**: Should start with `sk-`
2. **Verify key is active**: Check OpenAI dashboard
3. **Check billing**: Ensure account has credits
4. **Regenerate key**: Create new key if needed

### Tavily API Key Issues

#### Issue: "Tavily API key invalid"
```
ERROR: Invalid Tavily API key
```

**Solution:**
```bash
# Get new API key from Tavily dashboard
# Update .env file
TAVILY_API_KEY=your_tavily_api_key_here

# Test API key
python -c "
from tavily import TavilyClient
client = TavilyClient(api_key='your_key')
print('API key valid')
"
```

## 🗄️ Database Issues

### Vector Database Problems

#### Issue: "ChromaDB connection failed"
```
ERROR: Could not connect to ChromaDB
```

**Solution:**
```bash
# Check database directory
ls -la data/vectorstore/

# Recreate database
rm -rf data/vectorstore/
python scripts/setup_vectorstore.py

# Check permissions
chmod -R 755 data/vectorstore/
```

#### Issue: "Collection not found"
```
ERROR: Collection 'Aara_knowledge' not found
```

**Solution:**
```bash
# Initialize vector database
python scripts/setup_vectorstore.py

# Verify collection exists
python -c "
import chromadb
client = chromadb.PersistentClient(path='data/vectorstore')
print(client.list_collections())
"
```

### Database Corruption

#### Issue: "Database file corrupted"
```
ERROR: Database file is corrupted
```

**Solution:**
```bash
# Backup existing data (if possible)
cp -r data/vectorstore data/vectorstore.backup

# Remove corrupted database
rm -rf data/vectorstore/

# Reinitialize database
python scripts/setup_vectorstore.py

# Verify database integrity
python -c "
import chromadb
client = chromadb.PersistentClient(path='data/vectorstore')
collection = client.get_collection('Aara_knowledge')
print(f'Collection has {collection.count()} documents')
"
```

## 🔤 Encoding Issues

### UTF-8 Encoding Problems

#### Issue: "UnicodeDecodeError: 'charmap' codec can't decode"
```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 1234
```

**Solution:**
```bash
# Set environment variable (Windows)
set PYTHONIOENCODING=utf-8

# PowerShell
$env:PYTHONIOENCODING="utf-8"

# Linux/macOS
export PYTHONIOENCODING=utf-8

# Permanent fix - add to shell profile
echo 'export PYTHONIOENCODING=utf-8' >> ~/.bashrc
source ~/.bashrc
```

#### Issue: "Emoji chAaracters not displaying"
```
ERROR: 'ascii' codec can't encode chAaracter
```

**Solution:**
```bash
# Windows Command Prompt
chcp 65001

# PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Verify encoding
python -c "import sys; print(sys.stdout.encoding)"
```

### File Encoding Issues

#### Issue: "Rules files not loading properly"
```
ERROR: Could not parse JSON file
```

**Solution:**
```python
# Check file encoding
file -I rules/general_rules.json

# Fix encoding in rules_engine.py (already fixed)
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
```

## 🚀 Runtime Issues

### Memory Problems

#### Issue: "Out of memory error"
```
ERROR: MemoryError
```

**Solution:**
```bash
# Check memory usage
python -c "
import psutil
print(f'Memory usage: {psutil.virtual_memory().percent}%')
"

# Reduce memory usage
# Edit config/settings.yaml
agent:
  max_history: 5  # Reduce from 10
  max_tokens: 500  # Reduce from 1000

# Clear cache
python -c "
import os
import shutil
cache_dir = '__pycache__'
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
"
```

### Performance Issues

#### Issue: "Agent responses are very slow"
```
WARNING: Response time exceeded 30 seconds
```

**Solutions:**
1. **Check internet connection**
2. **Verify API key limits**
3. **Reduce response complexity**
4. **Enable caching**

```yaml
# config/settings.yaml
performance:
  enable_caching: true
  cache_ttl: 3600
  max_concurrent_requests: 5

api:
  openai:
    timeout: 15
    max_tokens: 500
```

### Rule Processing Issues

#### Issue: "Rules not matching expected patterns"
```
WARNING: No rules matched for input
```

**Solution:**
```bash
# Test rules engine
python test_expanded_rules.py

# Check rule files
python -c "
from rules.rules_engine import RulesEngine
engine = RulesEngine()
result = engine.process_rules('hello')
print(result)
"

# Verify rule file integrity
python -c "
import json
with open('rules/general_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)
    print(f'Loaded {len(rules)} rule categories')
"
```

## 🌐 Network Issues

### API Connection Problems

#### Issue: "Connection timeout to OpenAI"
```
ERROR: Request timed out
```

**Solution:**
```bash
# Test internet connectivity
ping api.openai.com

# Check firewall/proxy settings
# Increase timeout in config
api:
  openai:
    timeout: 60  # Increase from 30

# Test API connection
python -c "
import openai
client = openai.OpenAI()
response = client.models.list()
print('OpenAI connection successful')
"
```

#### Issue: "SSL certificate verification failed"
```
ERROR: SSL certificate verify failed
```

**Solution:**
```bash
# Update certificates
# macOS
/Applications/Python\ 3.9/Install\ Certificates.command

# Linux
sudo apt-get update && sudo apt-get install ca-certificates

# Windows - Update Windows and Python

# Temporary workaround (not recommended for production)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

## 🔧 Configuration Issues

### YAML Configuration Problems

#### Issue: "YAML parsing error"
```
ERROR: Could not parse YAML configuration
```

**Solution:**
```bash
# Validate YAML syntax
python -c "
import yaml
with open('config/settings.yaml', 'r') as f:
    try:
        config = yaml.safe_load(f)
        print('YAML is valid')
    except yaml.YAMLError as e:
        print(f'YAML error: {e}')
"

# Common YAML issues:
# - Incorrect indentation (use spaces, not tabs)
# - Missing colons
# - Unquoted special chAaracters
```

### Environment Variable Issues

#### Issue: "Environment variables not loading"
```
ERROR: Configuration value not found
```

**Solution:**
```bash
# Check .env file format
cat .env

# Verify no spaces around equals sign
OPENAI_API_KEY=your_key_here  # Correct
OPENAI_API_KEY = your_key_here  # Incorrect

# Test environment loading
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv('OPENAI_API_KEY'))
"
```

## 🧪 Testing Issues

### Test Failures

#### Issue: "Tests failing with import errors"
```
ERROR: ModuleNotFoundError in tests
```

**Solution:**
```bash
# Run tests from project root
cd aAara-health-agent
python -m pytest tests/ -v

# Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Install in development mode
pip install -e .
```

#### Issue: "Mock API responses not working"
```
ERROR: Real API calls in tests
```

**Solution:**
```python
# Create test configuration
# test_config.yaml
services:
  openai:
    mock: true
  tavily:
    mock: true

# Use test configuration
python -c "
import os
os.environ['ENVIRONMENT'] = 'test'
# Run tests
"
```

## 📊 Monitoring Issues

### Logging Problems

#### Issue: "Log files not being created"
```
ERROR: Permission denied writing to log file
```

**Solution:**
```bash
# Create logs directory
mkdir -p logs

# Set permissions
chmod 755 logs

# Check disk space
df -h

# Test logging
python -c "
import logging
logging.basicConfig(
    filename='logs/test.log',
    level=logging.INFO
)
logging.info('Test log message')
print('Log test complete')
"
```

### Performance Monitoring

#### Issue: "High CPU usage"
```
WARNING: CPU usage above 80%
```

**Solution:**
```bash
# Monitor Python processes
top -p $(pgrep python)

# Check for infinite loops
python -c "
import cProfile
import pstats
# Profile your code
"

# Optimize configuration
performance:
  max_concurrent_requests: 2  # Reduce from 10
  request_timeout: 15  # Reduce from 30
```

## 🆘 Emergency Procedures

### Complete Reset

If all else fails, perform a complete reset:

```bash
# 1. Backup important data
cp .env .env.backup
cp -r data/vectorstore data/vectorstore.backup

# 2. Clean installation
rm -rf venv/
rm -rf data/vectorstore/
rm -rf __pycache__/
rm -rf *.pyc

# 3. Fresh installation
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt

# 4. Restore configuration
cp .env.backup .env

# 5. Reinitialize database
python scripts/setup_vectorstore.py

# 6. Test installation
python quick_test.py
```

### Getting Help

If you're still experiencing issues:

1. **Check logs**: `logs/Aara.log` and `logs/Aara_errors.log`
2. **Run diagnostics**: `python -m Aara.diagnostics`
3. **Create issue**: [GitHub Issues](https://github.com/your-org/aAara-health-agent/issues)
4. **Join discussions**: [GitHub Discussions](https://github.com/your-org/aAara-health-agent/discussions)
5. **Contact support**: support@hermirror.com

### Diagnostic Information

When reporting issues, include:

```bash
# System information
python --version
pip --version
uname -a  # Linux/macOS
systeminfo  # Windows

# Package versions
pip list | grep -E "(langchain|openai|chromadb)"

# Configuration (remove sensitive data)
cat config/settings.yaml

# Recent logs
tail -50 logs/Aara.log
```

Remember: Most issues are configuration-related and can be resolved by carefully following the installation and setup guides. Don't hesitate to ask for help! 