from typing import Dict, Any

def response_node(llm):
    """Node that generates the final response with disclaimers."""
    def node(state: Dict[str, Any]) -> Dict[str, Any]:
        # Check if we already have a final response from rules or tools
        if state.get('final_response'):
            # Just ensure disclaimer is appended
            response = state['final_response']
            if 'consult a doctor' not in response.lower():
                response += "\n\n_Consult a doctor for medical advice._"
            state['final_response'] = response
            return state
        
        # Generate response using LLM
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
        
        # Always append medical disclaimer
        disclaimer = "\n\n_Consult a doctor for medical advice._"
        if 'consult a doctor' not in response_text.lower():
            response_text += disclaimer
        
        state['final_response'] = response_text
        return state
    
    return node 