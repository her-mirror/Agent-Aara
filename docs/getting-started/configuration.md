# Configuration Guide

## 🔧 Overview

The Ara Health Agent is highly configurable to meet different deployment needs, from development to production environments. This guide covers all configuration options and best practices.

## 📁 Configuration Files

### File Structure
```
config/
├── settings.yaml       # Main application settings
├── logging.yaml        # Logging configuration
└── .env               # Environment variables (not in repo)
```

## 🌍 Environment Variables (.env)

### Core Configuration
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4                    # or gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7                # 0.0-2.0, creativity level
OPENAI_MAX_TOKENS=1000                # Response length limit
OPENAI_TIMEOUT=30                     # Request timeout in seconds

# Tavily Search Configuration
TAVILY_API_KEY=your_tavily_api_key_here
TAVILY_MAX_RESULTS=5                  # Number of search results
TAVILY_INCLUDE_DOMAINS=               # Comma-separated domains to include
TAVILY_EXCLUDE_DOMAINS=               # Comma-separated domains to exclude
TAVILY_TIMEOUT=10                     # Search timeout in seconds

# Agent Configuration
AGENT_NAME=Ara                        # Agent display name
AGENT_DESCRIPTION=Your AI companion for women's health and skincare
AGENT_PERSONALITY=empathetic          # empathetic, professional, casual
AGENT_RESPONSE_STYLE=supportive       # supportive, clinical, educational
AGENT_MAX_HISTORY=10                  # Conversation history limit
```

### Database Configuration
```env
# Vector Database
VECTOR_DB_PATH=data/vectorstore       # Database storage path
VECTOR_DB_COLLECTION=ara_knowledge    # Collection name
VECTOR_DB_EMBEDDING_MODEL=text-embedding-ada-002
VECTOR_DB_CHUNK_SIZE=1000             # Text chunk size for embeddings
VECTOR_DB_CHUNK_OVERLAP=200           # Overlap between chunks

# Caching
ENABLE_CACHING=true                   # Enable response caching
CACHE_TTL=3600                        # Cache time-to-live (seconds)
CACHE_MAX_SIZE=1000                   # Maximum cache entries
CACHE_BACKEND=memory                  # memory, redis, file
```

### Safety Configuration
```env
# Safety Systems
ENABLE_SAFETY_CHECKS=true             # Enable all safety checks
ENABLE_EMERGENCY_DETECTION=true       # Emergency situation detection
ENABLE_CRISIS_INTERVENTION=true       # Crisis intervention resources
ENABLE_CONTENT_FILTERING=true         # Content filtering
ENABLE_MEDICAL_DISCLAIMERS=true       # Add medical disclaimers

# Safety Thresholds
SAFETY_CONFIDENCE_THRESHOLD=0.8       # Safety detection confidence
EMERGENCY_RESPONSE_DELAY=0            # Delay before emergency response
CRISIS_ESCALATION_THRESHOLD=0.9       # Crisis escalation threshold
```

### Performance Configuration
```env
# Performance Tuning
MAX_CONCURRENT_REQUESTS=10            # Concurrent request limit
REQUEST_TIMEOUT=30                    # Request timeout
RATE_LIMIT_REQUESTS=100               # Requests per minute
RATE_LIMIT_WINDOW=60                  # Rate limit window (seconds)

# Memory Management
MAX_MEMORY_USAGE=2048                 # Max memory usage (MB)
GARBAGE_COLLECTION_INTERVAL=300       # GC interval (seconds)
```

### Logging Configuration
```env
# Logging Settings
LOG_LEVEL=INFO                        # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/ara.log                 # Log file path
LOG_MAX_SIZE=10485760                 # Max log file size (10MB)
LOG_BACKUP_COUNT=5                    # Number of backup files
LOG_FORMAT=detailed                   # simple, detailed, json
LOG_CONSOLE_OUTPUT=true               # Enable console logging
```

## ⚙️ Application Settings (settings.yaml)

### Main Configuration File
```yaml
# Agent Configuration
agent:
  name: "Ara"
  description: "Your AI companion for women's health and skincare"
  personality: "empathetic"           # empathetic, professional, casual
  response_style: "supportive"        # supportive, clinical, educational
  max_tokens: 1000                    # Maximum response length
  temperature: 0.7                    # Response creativity (0.0-2.0)
  max_history: 10                     # Conversation history limit
  
  # Personality traits
  traits:
    empathy_level: "high"             # high, medium, low
    formality_level: "casual"         # formal, casual, mixed
    humor_level: "light"              # none, light, moderate
    cultural_sensitivity: "high"      # high, medium, low

# Safety Configuration
safety:
  emergency_detection: true           # Enable emergency detection
  crisis_intervention: true           # Enable crisis intervention
  medical_disclaimers: true           # Add medical disclaimers
  content_filtering: true             # Enable content filtering
  
  # Safety thresholds
  thresholds:
    emergency_confidence: 0.8         # Emergency detection confidence
    crisis_confidence: 0.9            # Crisis detection confidence
    safety_override: false            # Allow safety overrides
  
  # Emergency contacts
  emergency_resources:
    - name: "911"
      number: "911"
      description: "Emergency services"
    - name: "988 Suicide & Crisis Lifeline"
      number: "988"
      description: "24/7 crisis support"

# Features Configuration
features:
  search_enabled: true                # Enable search functionality
  personalization: true               # Enable personalization
  conversation_memory: true           # Enable conversation memory
  multi_language: false               # Enable multi-language support
  voice_interface: false              # Enable voice interface
  web_interface: true                 # Enable web interface
  
  # Feature flags
  experimental:
    advanced_reasoning: false         # Enable advanced reasoning
    predictive_health: false          # Enable predictive health insights
    integration_apis: false           # Enable third-party integrations

# Tools Configuration
tools:
  health_advice:
    enabled: true                     # Enable health advice tool
    max_response_length: 800          # Maximum response length
    include_disclaimers: true         # Include medical disclaimers
    confidence_threshold: 0.7         # Confidence threshold for advice
    
    # Specialized areas
    specializations:
      - "menstrual_health"
      - "pcos_management"
      - "fertility_support"
      - "hormonal_health"
      - "mental_wellness"
  
  skincare:
    enabled: true                     # Enable skincare tool
    routine_complexity: "moderate"    # simple, moderate, advanced
    product_recommendations: true     # Enable product recommendations
    ingredient_analysis: true         # Enable ingredient analysis
    
    # Skin types supported
    skin_types:
      - "normal"
      - "oily"
      - "dry"
      - "combination"
      - "sensitive"
      - "acne_prone"
  
  search:
    enabled: true                     # Enable search tool
    max_results: 5                    # Maximum search results
    source_verification: true         # Verify source credibility
    real_time_updates: true           # Enable real-time information
    
    # Search domains
    trusted_domains:
      - "mayoclinic.org"
      - "webmd.com"
      - "healthline.com"
      - "nih.gov"
      - "who.int"

# Database Configuration
database:
  vector_store:
    provider: "chromadb"              # chromadb, pinecone, weaviate
    collection_name: "ara_knowledge"  # Collection name
    embedding_model: "text-embedding-ada-002"
    chunk_size: 1000                  # Text chunk size
    chunk_overlap: 200                # Overlap between chunks
    
  cache:
    enabled: true                     # Enable caching
    backend: "memory"                 # memory, redis, file
    ttl: 3600                         # Time-to-live (seconds)
    max_size: 1000                    # Maximum cache entries

# API Configuration
api:
  openai:
    model: "gpt-4"                    # OpenAI model
    temperature: 0.7                  # Response creativity
    max_tokens: 1000                  # Maximum tokens
    timeout: 30                       # Request timeout
    
  tavily:
    max_results: 5                    # Maximum search results
    timeout: 10                       # Search timeout
    include_answer: true              # Include direct answers
    include_raw_content: false        # Include raw content

# Performance Configuration
performance:
  max_concurrent_requests: 10         # Concurrent request limit
  request_timeout: 30                 # Request timeout
  rate_limiting:
    enabled: true                     # Enable rate limiting
    requests_per_minute: 100          # Requests per minute
    burst_limit: 20                   # Burst request limit
  
  memory_management:
    max_memory_mb: 2048               # Maximum memory usage
    gc_interval: 300                  # Garbage collection interval
    
  optimization:
    enable_response_streaming: true   # Enable streaming responses
    enable_request_batching: false    # Enable request batching
    enable_model_caching: true        # Enable model caching
```

## 📝 Logging Configuration (logging.yaml)

### Comprehensive Logging Setup
```yaml
version: 1
disable_existing_loggers: false

formatters:
  simple:
    format: '%(levelname)s - %(message)s'
  
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
    datefmt: '%Y-%m-%d %H:%M:%S'
  
  json:
    format: '{"timestamp": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "module": "%(module)s", "function": "%(funcName)s", "message": "%(message)s"}'
    datefmt: '%Y-%m-%d %H:%M:%S'

filters:
  health_filter:
    (): 'utils.logging_filters.HealthDataFilter'
  
  safety_filter:
    (): 'utils.logging_filters.SafetyEventFilter'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout
  
  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: detailed
    filename: logs/ara.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    encoding: utf-8
  
  error_file:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: detailed
    filename: logs/ara_errors.log
    maxBytes: 10485760  # 10MB
    backupCount: 3
    encoding: utf-8
  
  safety_file:
    class: logging.handlers.RotatingFileHandler
    level: WARNING
    formatter: json
    filename: logs/ara_safety.log
    maxBytes: 10485760  # 10MB
    backupCount: 10
    encoding: utf-8
    filters: [safety_filter]

loggers:
  ara.agent:
    level: DEBUG
    handlers: [console, file]
    propagate: false
  
  ara.rules:
    level: DEBUG
    handlers: [console, file]
    propagate: false
  
  ara.tools:
    level: DEBUG
    handlers: [console, file]
    propagate: false
  
  ara.safety:
    level: WARNING
    handlers: [console, file, safety_file]
    propagate: false
  
  openai:
    level: WARNING
    handlers: [file]
    propagate: false
  
  chromadb:
    level: WARNING
    handlers: [file]
    propagate: false

root:
  level: INFO
  handlers: [console, file, error_file]
```

## 🔐 Security Configuration

### Environment-Specific Settings

#### Development Environment
```yaml
# development.yaml
environment: development
debug: true
safety:
  emergency_detection: true
  crisis_intervention: true
  content_filtering: false    # Relaxed for testing
logging:
  level: DEBUG
  console_output: true
performance:
  rate_limiting:
    enabled: false            # Disabled for development
```

#### Production Environment
```yaml
# production.yaml
environment: production
debug: false
safety:
  emergency_detection: true
  crisis_intervention: true
  content_filtering: true
  safety_override: false      # No safety overrides in production
logging:
  level: INFO
  console_output: false
performance:
  rate_limiting:
    enabled: true
    requests_per_minute: 60   # Stricter limits
  security:
    api_key_rotation: true
    request_validation: strict
```

### Security Best Practices
```yaml
security:
  api_keys:
    rotation_interval: 2592000  # 30 days
    encryption: true
    storage: "environment"      # environment, vault, file
  
  request_validation:
    enabled: true
    max_request_size: 10240     # 10KB
    allowed_content_types:
      - "application/json"
      - "text/plain"
  
  rate_limiting:
    enabled: true
    per_ip_limit: 100
    per_user_limit: 1000
    window_size: 3600           # 1 hour
  
  monitoring:
    failed_requests_threshold: 10
    suspicious_activity_detection: true
    audit_logging: true
```

## 🎯 Customization Options

### Personality Customization
```yaml
personality:
  base_personality: "empathetic"
  
  # Communication style
  communication:
    tone: "warm"                # warm, professional, casual
    formality: "semi-formal"    # formal, semi-formal, casual
    emoji_usage: "moderate"     # none, light, moderate, heavy
    
  # Response characteristics
  responses:
    length_preference: "detailed"  # brief, moderate, detailed
    explanation_level: "thorough"  # basic, moderate, thorough
    examples_included: true        # Include examples in responses
    
  # Cultural adaptations
  cultural:
    sensitivity_level: "high"      # high, medium, low
    inclusive_language: true       # Use inclusive language
    cultural_references: "minimal" # none, minimal, moderate
```

### Domain-Specific Configuration
```yaml
domains:
  health:
    # Medical disclaimer settings
    disclaimers:
      always_include: true
      custom_text: "This information is for educational purposes only..."
      
    # Specialization focus
    focus_areas:
      - weight: 0.3
        area: "reproductive_health"
      - weight: 0.2
        area: "mental_wellness"
      - weight: 0.2
        area: "hormonal_health"
      - weight: 0.15
        area: "nutrition"
      - weight: 0.15
        area: "fitness"
  
  skincare:
    # Product recommendation settings
    recommendations:
      budget_consideration: true
      ingredient_sensitivity: true
      routine_complexity: "adaptive"  # simple, adaptive, advanced
      
    # Skin type focus
    skin_type_weights:
      sensitive: 0.25
      acne_prone: 0.25
      dry: 0.2
      oily: 0.15
      combination: 0.1
      normal: 0.05
```

## 🔄 Configuration Management

### Environment-Based Configuration
```python
# config/config_manager.py
import os
import yaml
from typing import Dict, Any

class ConfigManager:
    def __init__(self, env: str = None):
        self.env = env or os.getenv('ENVIRONMENT', 'development')
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration based on environment"""
        base_config = self._load_yaml('config/settings.yaml')
        env_config = self._load_yaml(f'config/{self.env}.yaml')
        
        # Merge configurations
        return self._merge_configs(base_config, env_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
```

### Dynamic Configuration Updates
```python
# config/dynamic_config.py
class DynamicConfig:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.watchers = {}
    
    def watch(self, key: str, callback):
        """Watch for configuration changes"""
        if key not in self.watchers:
            self.watchers[key] = []
        self.watchers[key].append(callback)
    
    def update(self, key: str, value: Any):
        """Update configuration value"""
        self.config_manager.set(key, value)
        
        # Notify watchers
        if key in self.watchers:
            for callback in self.watchers[key]:
                callback(key, value)
```

## 🧪 Testing Configuration

### Test Environment Settings
```yaml
# test.yaml
environment: test
debug: true

# Use mock services for testing
services:
  openai:
    mock: true
    mock_responses: "test_data/mock_responses.json"
  
  tavily:
    mock: true
    mock_results: "test_data/mock_search_results.json"

# Test-specific database
database:
  vector_store:
    collection_name: "test_ara_knowledge"
    path: "test_data/vectorstore"

# Relaxed safety for testing
safety:
  emergency_detection: false
  crisis_intervention: false
  content_filtering: false

# Fast responses for testing
performance:
  request_timeout: 5
  max_concurrent_requests: 1
```

## 📊 Monitoring Configuration

### Health Checks
```yaml
monitoring:
  health_checks:
    enabled: true
    interval: 30              # seconds
    endpoints:
      - name: "database"
        check: "database_connection"
      - name: "openai"
        check: "api_connectivity"
      - name: "memory"
        check: "memory_usage"
  
  metrics:
    enabled: true
    export_interval: 60       # seconds
    metrics_port: 9090
    
  alerts:
    enabled: true
    channels:
      - type: "email"
        address: "admin@hermirror.com"
      - type: "slack"
        webhook: "${SLACK_WEBHOOK_URL}"
```

## 🚀 Deployment Configuration

### Docker Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  ara-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
    restart: unless-stopped
    
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

This comprehensive configuration system allows you to customize every aspect of the Ara Health Agent while maintaining security, performance, and reliability across different deployment environments. 