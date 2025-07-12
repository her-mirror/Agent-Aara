import os
from typing import Dict, Any

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

def response_node(llm):
    """Node that generates the final response with disclaimers."""
    def node(state: Dict[str, Any]) -> Dict[str, Any]:
        # Check if we already have a final response from rules or tools
        if state.get('final_response'):
            # Just ensure disclaimer is appended for medical content
            response = state['final_response']
            if 'consult a doctor' not in response.lower() and not any(keyword in response.lower() 
                for keyword in ['crisis', 'emergency', '911', '988', 'suicide']):
                response += "\n\n_Consult a doctor for medical advice._"
            state['final_response'] = response
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
                # Default LLM response
                context = f"""
                User input: {user_input}
                Chat history: {chat_history}
                
                You are Ara, an empathetic AI agent specializing in women's health and skincare. 
                Provide a helpful, accurate, and supportive response. 
                Be empathetic and non-judgmental.
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
                # Add medical disclaimer for other responses
                if 'consult a doctor' not in response_text.lower():
                    response_text += "\n\n_Consult a doctor for medical advice._"
            
            state['final_response'] = response_text
            return state
        
        # Generate response using LLM for non-rule-based queries
        user_input = state.get('user_input', '')
        steps = state.get('intermediate_steps', [])
        chat_history = state.get('chat_history', [])
        
        # Create context for LLM
        context = f"""
        User input: {user_input}
        Chat history: {chat_history}
        Processing steps: {steps}
        
        You are Ara, an empathetic AI agent specializing in women's health and skincare. 
        Provide a helpful, accurate, and supportive response. 
        Be empathetic and non-judgmental.
        """
        
        try:
            response = llm.invoke(context)
            response_text = response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            print(f"Error generating response: {e}")
            response_text = "I apologize, but I'm having trouble processing your request right now. Please try again."
        
        # Always append medical disclaimer for general responses
        disclaimer = "\n\n_Consult a doctor for medical advice._"
        if 'consult a doctor' not in response_text.lower():
            response_text += disclaimer
        
        state['final_response'] = response_text
        return state
    
    return node 