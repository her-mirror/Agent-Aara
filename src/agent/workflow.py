import os
import sys
import yaml
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agent.reasoning import reasoning_node
from src.agent.response import response_node
from rules.rules_engine import rule_engine_node
from tools.skincare import skincare_tool
from tools.health_advice import health_advice_tool
from tools.search import search_tool
from tools.product_suggestion import product_suggestion_tool

# Load environment variables and config
load_dotenv()

# Load config with proper path handling
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'settings.yaml')
with open(config_path, 'r') as f:
    settings = yaml.safe_load(f)

MODEL_NAME = settings.get('llm', {}).get('model_name', 'gpt-4o')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

llm = ChatOpenAI(model=MODEL_NAME, api_key=OPENAI_API_KEY)

# Define the state type for the workflow
class WorkflowState(TypedDict, total=False):
    user_input: str
    chat_history: List[Dict[str, str]]
    intermediate_steps: List[Dict[str, Any]]
    final_response: str
    next_node: str
    use_llm: bool
    response_type: str
    route_to: str

# Create workflow graph
workflow = StateGraph(WorkflowState)

# Add nodes
workflow.add_node("reasoning", reasoning_node(llm))
workflow.add_node("rule_engine", rule_engine_node)
workflow.add_node("skincare_tool", skincare_tool)
workflow.add_node("health_advice_tool", health_advice_tool)
workflow.add_node("search_tool", search_tool)
workflow.add_node("product_suggestion", product_suggestion_tool)
workflow.add_node("response", response_node(llm))

# Set entry point
workflow.set_entry_point("reasoning")

# Add conditional edges based on reasoning output
def route_after_reasoning(state: WorkflowState) -> str:
    return state.get("next_node", "rule_engine")

def route_after_rules(state: WorkflowState) -> str:
    if state.get("final_response"):
        return "response"
    # Check if LLM should generate response (greeting, crisis, etc.)
    if state.get("use_llm"):
        return "response"
    next_node = state.get("next_node", "response")
    return next_node

# Add edges
workflow.add_conditional_edges(
    "reasoning",
    route_after_reasoning,
    {
        "rule_engine": "rule_engine",
        "skincare_tool": "skincare_tool",
        "health_advice_tool": "health_advice_tool",
        "search_tool": "search_tool",
        "product_suggestion": "product_suggestion",
        "response": "response"
    }
)

workflow.add_conditional_edges(
    "rule_engine",
    route_after_rules,
    {
        "skincare_tool": "skincare_tool",
        "health_advice_tool": "health_advice_tool",
        "search_tool": "search_tool",
        "product_suggestion": "product_suggestion",
        "response": "response"
    }
)

workflow.add_edge("skincare_tool", "product_suggestion")
workflow.add_edge("health_advice_tool", "product_suggestion")
workflow.add_edge("search_tool", "product_suggestion")
workflow.add_edge("product_suggestion", "response")
workflow.add_edge("response", END)

# Compile the workflow
app = workflow.compile()

def run_workflow(user_input: str, chat_history: List[Dict[str, str]] = None) -> str:
    """Run the workflow with user input and return the final response."""
    if chat_history is None:
        chat_history = []
    
    initial_state = {
        "user_input": user_input,
        "chat_history": chat_history,
        "intermediate_steps": [],
        "final_response": "",
        "next_node": "",
        "use_llm": False,
        "response_type": "",
        "route_to": ""
    }
    
    try:
        result = app.invoke(initial_state)
        return result.get('final_response', 'Sorry, I could not process your request.')
    except Exception as e:
        print(f"Error in workflow: {e}")
        # Fallback to direct LLM response for any errors
        try:
            fallback_context = f"""
            You are Ara, an empathetic AI agent specializing in women's health and skincare.
            
            User input: {user_input}
            Chat history: {chat_history}
            
            The user said: "{user_input}"
            
            Please provide an appropriate response. If this is:
            - A casual greeting/conversation: Respond warmly and redirect to health/skincare topics
            - A health/skincare question: Provide helpful guidance
            - Something unclear: Ask for clarification in a supportive way
            
            Be empathetic and helpful.
            """
            
            fallback_response = llm.invoke(fallback_context)
            response_text = fallback_response.content if hasattr(fallback_response, 'content') else str(fallback_response)
            
            # Add disclaimer if it's health-related
            if any(word in user_input.lower() for word in ['health', 'skin', 'period', 'symptom', 'pain', 'advice']):
                if 'consult a doctor' not in response_text.lower():
                    response_text += "\n\n_Consult a doctor for medical advice._"
            
            return response_text
        except Exception as fallback_error:
            print(f"Fallback error: {fallback_error}")
            return "I'm sorry, I'm having some technical difficulties. Please try asking your question again, and I'll do my best to help you with your health and skincare needs." 