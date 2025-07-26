import os
import yaml
from typing import Dict, Any

# Load settings
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'settings.yaml')
try:
    with open(config_path, 'r') as f:
        settings = yaml.safe_load(f)
except:
    settings = {'verification': {'enabled': True}}  # Default to enabled if config not found

def load_prompt(prompt_file: str) -> str:
    """Load a prompt from the prompts directory"""
    prompts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'prompts')
    try:
        with open(os.path.join(prompts_dir, prompt_file), 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ Prompt file not found: {prompt_file}")
        return ""
    except Exception as e:
        print(f"❌ Error loading prompt: {e}")
        return ""

def verify_response(llm, user_question: str, generated_response: str) -> str:
    """
    Verify if the generated response is appropriate for the user's question.
    Returns improved response if needed, otherwise returns original response.
    """
    # Check if verification is enabled
    if not settings.get('verification', {}).get('enabled', True):
        return generated_response  # Skip verification if disabled
    
    verification_prompt = load_prompt('verification_prompt.txt')
    
    if not verification_prompt:
        return generated_response  # Fallback if prompt not found
    
    # Create verification request
    verification_request = f"""
{verification_prompt}

## Current Case to Verify:

**USER'S ORIGINAL QUESTION**: "{user_question}"

**GENERATED RESPONSE**: "{generated_response}"

**YOUR VERIFICATION**:
"""
    
    try:
        # Get LLM verification
        verification_result = llm.invoke(verification_request)
        verification_content = verification_result.content if hasattr(verification_result, 'content') else str(verification_result)
        
        # Parse verification result
        if "VERIFICATION: APPROVED" in verification_content:
            return generated_response  # Original response is good
        elif "VERIFICATION: NEEDS_IMPROVEMENT" in verification_content:
            # Extract improved response
            if "IMPROVED_RESPONSE:" in verification_content:
                improved_part = verification_content.split("IMPROVED_RESPONSE:")[1].strip()
                # Remove any trailing formatting
                improved_response = improved_part.replace("```", "").strip()
                return improved_response
            else:
                return generated_response  # Fallback
        else:
            return generated_response  # Fallback if parsing fails
            
    except Exception as e:
        print(f"Error in response verification: {e}")
        return generated_response  # Fallback to original response

def response_node(llm):
    """Node that generates the final response with disclaimers."""
    def node(state: Dict[str, Any]) -> Dict[str, Any]:
        user_input = state.get('user_input', '')
        chat_history = state.get('chat_history', [])
        
        print(f"\n📋 CHAT HISTORY IN RESPONSE NODE: {len(chat_history)} messages")
        if chat_history:
            for i, msg in enumerate(chat_history[-2:]):  # Show last 2 messages
                print(f"  {i+1}. User: {msg.get('user', '')[:40]}...")
                print(f"     Aara: {msg.get('Aara', '')[:40]}...")
        
        # Check if we already have a final response from rules or tools
        if state.get('final_response'):
            # Only add disclaimer if response contains medical advice
            response = state['final_response']
            if any(keyword in response.lower() for keyword in ['diagnosis', 'treatment', 'medication', 'symptoms', 'condition']):
                if 'consult a doctor' not in response.lower() and not any(keyword in response.lower() 
                    for keyword in ['crisis', 'emergency', '911', '988', 'suicide']):
                    response += "\n\n_Consult a doctor for medical advice._"
            
            # VERIFICATION STEP: Verify rule-based response
            verified_response = verify_response(llm, user_input, response)
            state['final_response'] = verified_response
            return state
        
        # Check if this should use LLM with specialized prompts
        if state.get('use_llm'):
            response_type = state.get('response_type', '')
            user_input = state.get('user_input', '')
            chat_history = state.get('chat_history', [])
            
            if response_type == 'greeting':
                # Use specialized greeting prompt
                greeting_prompt = load_prompt('greeting_prompt.txt')
                context = f"""
                {greeting_prompt}

                User's greeting: {user_input}
                Chat history: {chat_history}
                
                Generate a personalized, warm greeting response.
                """
                
            elif response_type == 'crisis':
                # Use specialized crisis prompt
                crisis_prompt = load_prompt('crisis_prompt.txt')
                context = f"""
                {crisis_prompt}

                User's message: {user_input}
                Chat history: {chat_history}
                
                Generate a compassionate, urgent crisis response that could save a life.
                """
                
            else:
                # Use conversational prompt for natural responses
                conversational_prompt = load_prompt('conversational_prompt.txt')
                context = f"""
                {conversational_prompt}

                User's message: {user_input}
                Chat history: {chat_history}
                
                Respond naturally as Aara, offering to help with specific topics based on what they mentioned.
                """
            
            try:
                response = llm.invoke(context)
                response_text = response.content if hasattr(response, 'content') else str(response)
            except Exception as e:
                print(f"Error generating response: {e}")
                if response_type == 'crisis':
                    response_text = """I'm very concerned about you. Please reach out for help immediately:

                    🚨 **Crisis Resources (Available 24/7):**
                    - **988 Suicide & Crisis Lifeline**: Call or text 988
                    - **Crisis Text Line**: Text HOME to 741741
                    - **Emergency Services**: Call 911

                    You are not alone, and help is available. Please reach out right now."""
                else:
                    response_text = "I apologize, but I'm having trouble processing your request right now. Please try again."
            
            # Add appropriate disclaimers
            if response_type == 'crisis':
                # Don't add medical disclaimer for crisis responses
                pass
            elif response_type == 'greeting':
                # Don't add medical disclaimer for greetings
                pass
            else:
                # Only add medical disclaimer if the response contains medical advice
                if any(keyword in response_text.lower() for keyword in ['diagnosis', 'treatment', 'medication', 'symptoms', 'condition']):
                    if 'consult a doctor' not in response_text.lower():
                        response_text += "\n\n_Consult a doctor for medical advice._"
            
            # VERIFICATION STEP: Verify LLM-based response
            verified_response = verify_response(llm, user_input, response_text)
            state['final_response'] = verified_response
            return state
        
        # Generate response using LLM for non-rule-based queries
        user_input = state.get('user_input', '')
        steps = state.get('intermediate_steps', [])
        chat_history = state.get('chat_history', [])
        
        # Use conversational prompt for natural responses
        conversational_prompt = load_prompt('conversational_prompt.txt')
        context = f"""
        {conversational_prompt}

        User's message: {user_input}
        Chat history: {chat_history}
        Processing steps: {steps}
        
        Respond naturally as Aara, offering to help with specific topics based on what they mentioned.
        """
        
        try:
            response = llm.invoke(context)
            response_text = response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            print(f"Error generating response: {e}")
            response_text = "I apologize, but I'm having trouble processing your request right now. Please try again."
        
        # Only append medical disclaimer if response contains medical advice
        if any(keyword in response_text.lower() for keyword in ['diagnosis', 'treatment', 'medication', 'symptoms', 'condition']):
            if 'consult a doctor' not in response_text.lower():
                response_text += "\n\n_Consult a doctor for medical advice._"
        
        # VERIFICATION STEP: Verify general LLM response
        verified_response = verify_response(llm, user_input, response_text)
        state['final_response'] = verified_response
        return state
    
    return node 