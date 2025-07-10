import json
import os
from typing import Dict, List, Any, Optional

RULES_DIR = os.path.dirname(__file__)

def load_rules() -> tuple:
    """Load all rule files with proper UTF-8 encoding"""
    rules_dir = os.path.join(os.path.dirname(__file__))
    
    # Load each rule file with explicit UTF-8 encoding
    try:
        with open(os.path.join(rules_dir, 'health_rules.json'), 'r', encoding='utf-8') as f:
            health_rules = json.load(f)
        
        with open(os.path.join(rules_dir, 'skincare_rules.json'), 'r', encoding='utf-8') as f:
            skincare_rules = json.load(f)
        
        with open(os.path.join(rules_dir, 'safety_rules.json'), 'r', encoding='utf-8') as f:
            safety_rules = json.load(f)
        
        with open(os.path.join(rules_dir, 'general_rules.json'), 'r', encoding='utf-8') as f:
            general_rules = json.load(f)
        
        return health_rules, skincare_rules, safety_rules, general_rules
    
    except UnicodeDecodeError as e:
        print(f"❌ Unicode encoding error: {e}")
        print("💡 Solution: Files contain special characters that need UTF-8 encoding")
        raise
    except FileNotFoundError as e:
        print(f"❌ Rule file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        raise

health_rules, skincare_rules, safety_rules, general_rules = load_rules()

def rule_engine_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule-based decision engine that processes user input and returns appropriate responses.
    
    Priority order:
    1. Safety checks (highest priority)
    2. General rules (greetings, agent info, platform info)
    3. Health/skincare routing (lowest priority)
    """
    user_input = state.get("user_input", "").lower().strip()
    
    if not user_input:
        return state
    
    try:
        # Load rules with proper encoding
        health_rules, skincare_rules, safety_rules, general_rules = load_rules()
        
        # 1. SAFETY CHECKS (Highest Priority)
        # Check emergency situations first
        for emergency in safety_rules.get("emergencies", []):
            if emergency["trigger"].lower() in user_input:
                state["final_response"] = emergency["response"]
                return state
        
        # Check crisis resources
        for crisis in safety_rules.get("crisis_resources", []):
            if crisis["trigger"].lower() in user_input:
                state["final_response"] = crisis["response"]
                return state
        
        # Check general safety
        for safety in safety_rules.get("general_safety", []):
            if safety["trigger"].lower() in user_input:
                state["final_response"] = safety["response"]
                return state
        
        # 2. GENERAL RULES (Medium Priority)
        # Check greetings
        for greeting in general_rules.get("greetings", []):
            if greeting["trigger"].lower() in user_input:
                state["final_response"] = greeting["response"]
                return state
        
        # Check agent info
        for info in general_rules.get("agent_info", []):
            if info["trigger"].lower() in user_input:
                state["final_response"] = info["response"]
                return state
        
        # Check platform info
        for platform in general_rules.get("platform_info", []):
            if platform["trigger"].lower() in user_input:
                state["final_response"] = platform["response"]
                return state
        
        # Check capabilities
        for capability in general_rules.get("capabilities", []):
            if capability["trigger"].lower() in user_input:
                state["final_response"] = capability["response"]
                return state
        
        # Check conversation starters
        for starter in general_rules.get("conversation_starters", []):
            if starter["trigger"].lower() in user_input:
                state["final_response"] = starter["response"]
                return state
        
        # 3. HEALTH/SKINCARE ROUTING (Lower Priority)
        # Check health safety first
        for safety_check in health_rules.get("safety_checks", []):
            if safety_check["trigger"].lower() in user_input:
                state["final_response"] = safety_check["response"]
                return state
        
        # Check skincare safety
        for safety_check in skincare_rules.get("safety_checks", []):
            if safety_check["trigger"].lower() in user_input:
                state["final_response"] = safety_check["response"]
                return state
        
        # Route to appropriate tools
        # Check health redirects
        for redirect in health_rules.get("redirects", []):
            if redirect["trigger"].lower() in user_input:
                state["route_to"] = redirect["tool"]
                return state
        
        # Check skincare redirects
        for redirect in skincare_rules.get("redirects", []):
            if redirect["trigger"].lower() in user_input:
                state["route_to"] = redirect["tool"]
                return state
        
        # If no rules match, continue to next node
        return state
        
    except Exception as e:
        print(f"❌ Error in rule engine: {e}")
        # Fallback response
        state["final_response"] = "I'm here to help with your health and skincare questions. How can I assist you today?"
        return state 