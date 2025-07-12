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

def is_greeting(user_input: str) -> bool:
    """Check if user input is a greeting"""
    greeting_patterns = [
        'hello', 'hi', 'hey', 'good morning', 'good evening', 'good afternoon',
        'good night', 'howdy', 'greetings', 'hiya', "what's up", 'sup', 'yo',
        'bonjour', 'namaste', 'hola', 'salaam', 'good day'
    ]
    
    user_input_lower = user_input.lower().strip()
    
    # Remove common punctuation and extra characters
    cleaned_input = ''.join(c for c in user_input_lower if c.isalpha() or c.isspace())
    
    # Check for exact matches or greetings at the start
    for pattern in greeting_patterns:
        # Exact match
        if cleaned_input == pattern:
            return True
        # Starts with greeting
        if cleaned_input.startswith(pattern + ' '):
            return True
        # Check for repeated letters (hi -> hii, hello -> helloo)
        if len(cleaned_input) > len(pattern):
            # Check if it's a variation with repeated letters
            if cleaned_input.startswith(pattern) and all(c in pattern for c in cleaned_input):
                return True
    
    # Special handling for common greeting variations
    greeting_variants = {
        'hi': ['hii', 'hiii', 'hiiii'],
        'hello': ['helloo', 'hellooo', 'helloooo'],
        'hey': ['heyy', 'heyyy', 'heyyyy'],
        'yo': ['yoo', 'yooo']
    }
    
    for base, variants in greeting_variants.items():
        if cleaned_input in variants:
            return True
    
    return False

def is_crisis_situation(user_input: str) -> bool:
    """Check if user input indicates a mental health crisis"""
    crisis_patterns = [
        'suicide', 'kill myself', 'end my life', 'want to die', 'kill me',
        'hurt myself', 'self harm', 'end it all', 'not worth living',
        'better off dead', 'want to disappear', 'cut myself', 'overdose',
        'jump off', 'hang myself', 'shoot myself', 'drown myself',
        'life is not worth', 'tired of living', 'ready to die',
        'planning to kill', 'thinking about dying', 'thoughts of death',
        'suicidal thoughts', 'suicidal ideation', 'want to hurt myself'
    ]
    
    user_input_lower = user_input.lower().strip()
    
    for pattern in crisis_patterns:
        if pattern in user_input_lower:
            return True
    
    return False

health_rules, skincare_rules, safety_rules, general_rules = load_rules()

def rule_engine_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule-based decision engine that processes user input and returns appropriate responses.
    
    Priority order:
    1. Safety checks (highest priority)
    2. Crisis situations (enhanced LLM-based response)
    3. Greetings (dynamic LLM-based response)
    4. General rules (agent info, platform info)
    5. Health/skincare routing (lowest priority)
    """
    user_input = state.get("user_input", "").lower().strip()
    
    if not user_input:
        return state
    
    try:
        # Load rules with proper encoding
        health_rules, skincare_rules, safety_rules, general_rules = load_rules()
        
        # 1. SAFETY CHECKS (Highest Priority)
        # Check emergency situations first (but not mental health crises)
        for emergency in safety_rules.get("emergencies", []):
            # Skip suicide/crisis patterns - they will be handled by enhanced crisis system
            if emergency["trigger"].lower() in ['suicide', 'kill myself', 'end my life', 'want to die']:
                continue
            if emergency["trigger"].lower() in user_input:
                state["final_response"] = emergency["response"]
                return state
        
        # Check crisis resources (but allow specific crisis patterns to go to LLM)
        for crisis in safety_rules.get("crisis_resources", []):
            if crisis["trigger"].lower() in user_input:
                state["final_response"] = crisis["response"]
                return state
        
        # Check general safety
        for safety in safety_rules.get("general_safety", []):
            if safety["trigger"].lower() in user_input:
                state["final_response"] = safety["response"]
                return state
        
        # 2. CRISIS SITUATIONS (Enhanced LLM Response)
        if is_crisis_situation(state.get("user_input", "")):
            state["response_type"] = "crisis"
            state["use_llm"] = True
            return state
        
        # 3. GREETINGS (Dynamic LLM Response)
        if is_greeting(state.get("user_input", "")):
            state["response_type"] = "greeting"
            state["use_llm"] = True
            return state
        
        # 4. GENERAL RULES (Medium Priority)
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
        
        # 5. HEALTH/SKINCARE ROUTING (Lower Priority)
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