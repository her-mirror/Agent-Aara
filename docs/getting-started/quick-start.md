# Quick Start Guide

## 🚀 Get Ara Running in 5 Minutes

This guide will help you set up and run the Ara Health Agent locally in just a few minutes.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Git** for cloning the repository
- **OpenAI API Key** (for GPT-4 access)
- **Tavily API Key** (for search functionality)

## 🔧 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/aara-health-agent.git
cd aara-health-agent
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Tavily Search Configuration
TAVILY_API_KEY=your_tavily_api_key_here

# Agent Configuration
AGENT_NAME=Ara
AGENT_DESCRIPTION=Your AI companion for women's health and skincare

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/ara.log
```

### 5. Initialize the Vector Store

```bash
python scripts/setup_vectorstore.py
```

### 6. Run the Agent

```bash
python scripts/run_agent.py
```

## 🎯 First Interaction

Once the agent is running, you'll see:

```
🌸 Ara Health Agent Started
Type 'quit' to exit, 'help' for commands

You: 
```

Try these sample interactions:

### Basic Greeting
```
You: Hello Ara!
Ara: Hello! 🌸 I'm Ara, your AI companion for women's health and skincare. 
I'm here to provide personalized, empathetic support for your wellness journey...
```

### Health Question
```
You: I'm having irregular periods, what should I know?
Ara: I understand irregular periods can be concerning. Let me share some 
important information about menstrual irregularities...
```

### Skincare Query
```
You: What skincare routine is best for sensitive skin?
Ara: For sensitive skin, I recommend a gentle, minimalist approach. 
Here's a personalized routine that can help...
```

## 🔍 API Keys Setup

### Getting Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new secret key
5. Copy the key to your `.env` file

### Getting Your Tavily API Key

1. Visit [Tavily AI](https://tavily.com/)
2. Sign up for an account
3. Navigate to your dashboard
4. Generate an API key
5. Copy the key to your `.env` file

## 📁 Project Structure Overview

```
aara-health-agent/
├── src/agent/              # Core agent logic
│   ├── workflow.py         # LangGraph workflow
│   ├── reasoning.py        # AI reasoning logic
│   └── response.py         # Response generation
├── tools/                  # Specialized tools
│   ├── health_advice.py    # Health guidance tool
│   ├── skincare.py         # Skincare recommendations
│   └── search.py           # Search integration
├── rules/                  # Rule definitions
│   ├── safety_rules.json   # Emergency responses
│   ├── health_rules.json   # Health topic routing
│   ├── skincare_rules.json # Skincare topic routing
│   └── general_rules.json  # Greetings and info
├── data/                   # Knowledge base
│   └── health_data/        # Health information
├── config/                 # Configuration files
├── scripts/                # Utility scripts
└── tests/                  # Test files
```

## 🛠️ Configuration Options

### Agent Settings (`config/settings.yaml`)

```yaml
agent:
  name: "Ara"
  personality: "empathetic"
  response_style: "supportive"
  max_tokens: 1000
  temperature: 0.7

safety:
  emergency_detection: true
  crisis_intervention: true
  medical_disclaimers: true

features:
  search_enabled: true
  personalization: true
  conversation_memory: true
```

### Logging Configuration (`config/logging.yaml`)

```yaml
version: 1
formatters:
  default:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: default
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: default
    filename: logs/ara.log
```

## 🧪 Testing Your Installation

### Run Basic Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python -m pytest tests/test_rules.py -v
python -m pytest tests/test_workflow.py -v
```

### Test Individual Components

```bash
# Test rules engine
python test_simple.py

# Test expanded rules
python test_expanded_rules.py

# Test greetings
python test_greetings.py
```

### Quick Health Check

```bash
# Quick functionality test
python quick_test.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. API Key Errors
```
Error: OpenAI API key not found
```
**Solution**: Ensure your `.env` file contains valid API keys

#### 2. Module Import Errors
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Ensure virtual environment is activated and dependencies are installed

#### 3. UTF-8 Encoding Issues
```
UnicodeDecodeError: 'charmap' codec can't decode byte
```
**Solution**: This has been fixed in the latest version. Update your rules_engine.py

#### 4. Port Already in Use
```
Port 8000 is already in use
```
**Solution**: Change the port in configuration or kill the existing process

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set debug level in .env
LOG_LEVEL=DEBUG

# Or run with debug flag
python scripts/run_agent.py --debug
```

## 📚 Next Steps

Now that Ara is running, explore these resources:

1. **[Architecture Overview](../architecture/system-overview.md)** - Understand how Ara works
2. **[Rules Documentation](../rules/overview.md)** - Learn about the rule system
3. **[Adding Custom Rules](../development/adding-rules.md)** - Customize Ara's behavior
4. **[Tool Development](../development/creating-tools.md)** - Build new capabilities
5. **[API Reference](../api/workflow.md)** - Integrate with other systems

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs**: `logs/ara.log`
2. **Review troubleshooting**: [Common Issues](../troubleshooting/common-issues.md)
3. **Run tests**: Verify your installation with test suite
4. **GitHub Issues**: Report bugs and request features
5. **Community**: Join our discussions for support

## 🎉 Success!

You now have Ara running locally! The agent is ready to provide empathetic, personalized health and skincare guidance. Try different types of questions to explore Ara's capabilities.

### Sample Conversation Flow

```
You: Hi Ara, I'm new here
Ara: Welcome! I'm so glad you're here. I'm Ara, your AI companion for women's 
health and skincare. I'm here to provide personalized, empathetic support...

You: I have acne-prone skin and need a routine
Ara: I understand dealing with acne can be frustrating. Let me help you build 
a gentle yet effective routine for acne-prone skin...

You: What about hormonal acne?
Ara: Hormonal acne is very common and often related to menstrual cycles. 
Here's what you should know about managing hormonal breakouts...
```

Welcome to your journey with Ara! 🌸 