# Aara: Women's Health & Skincare AI Agent

Aara is an empathetic AI agent focused on women's health and skincare, built with LangGraph, LangChain, and a rule-based system for safe, accurate, and personalized responses. Aara answers queries about women's health (e.g., PCOS, menstrual cycles) and skincare (e.g., routines for oily skin), uses real-time web search, and maintains conversational memory for tailored advice.

---

## Features
- **Women's Health & Skincare Expertise**: Answers questions on PCOS, menstrual cycles, skincare routines, and more.
- **Rule-Based Safety**: Deterministic responses for common scenarios, safety checks, and disclaimers for medical queries.
- **Real-Time Data**: Integrates Tavily Search for up-to-date information.
- **Conversational Memory**: Remembers chat history for personalized advice.
- **Retrieval-Augmented Generation (RAG)**: Uses ChromaDB vectorstore for knowledge retrieval.
- **Modular & Extensible**: Easily add new tools, rules, or data sources.

---

## Project Structure
```
aAara-health-agent/
├── src/
│   ├── agent/
│   │   ├── workflow.py
│   │   ├── reasoning.py
│   │   ├── response.py
│   │   └── __init__.py
├── tools/
│   ├── skincare.py
│   ├── health_advice.py
│   ├── search.py
│   └── __init__.py
├── rules/
│   ├── rules_engine.py
│   ├── health_rules.json
│   ├── skincare_rules.json
│   ├── safety_rules.json
├── data/
│   ├── health_data/
│   │   ├── womens_health.txt
│   │   └── skincare_guides.txt
│   ├── vectorstore/
├── prompts/
│   ├── system_prompt.txt
│   ├── safety_prompt.txt
│   ├── clarification_prompt.txt
├── config/
│   ├── settings.yaml
│   ├── logging.yaml
├── tests/
│   ├── test_workflow.py
│   ├── test_rules.py
│   ├── test_tools.py
│   └── __init__.py
├── scripts/
│   ├── setup_vectorstore.py
│   ├── run_agent.py
├── .env
├── requirements.txt
├── README.md
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd aAara-health-agent
```

### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
- Copy `.env.example` to `.env` and add your API keys (OpenAI, Tavily, etc.).

### 4. Configure Settings
- Edit `config/settings.yaml` and `config/logging.yaml` as needed.

### 5. Initialize the Vectorstore
```bash
python scripts/setup_vectorstore.py
```

### 6. Run the Agent Locally
```bash
python scripts/run_agent.py
```

---

## Docker Deployment

### 1. Build and Run with Docker Compose
```bash
docker-compose up --build
```

### 2. Environment Variables
- Set environment variables in the Docker environment or use a `.env` file.

---

## Testing
```bash
pytest tests/
```

---

## Configuration
- **API Keys**: Store in `.env` (never hardcode).
- **Settings**: `config/settings.yaml` for agent and model config.
- **Logging**: `config/logging.yaml` for log levels and output.

---

## Safety & Disclaimers
- Aara always appends: _"Consult a doctor for medical advice."_
- Emergency queries (e.g., "severe pain") are flagged and redirected.
- All advice is informational, not a substitute for professional care.

---

## Extending Aara
- Add new rules in `rules/` JSON files.
- Add new tools in `tools/`.
- Add new data in `data/health_data/` and re-run `setup_vectorstore.py`.

---

## License
MIT 