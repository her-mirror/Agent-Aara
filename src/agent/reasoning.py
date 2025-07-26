from typing import Dict, Any

def reasoning_node(llm):
    """Node that analyzes user input and determines the next step."""
    def node(state: Dict[str, Any]) -> Dict[str, Any]:
        user_input = state['user_input']
        chat_history = state.get('chat_history', [])
        
        print(f"\n📋 CHAT HISTORY IN REASONING: {len(chat_history)} messages")
        if chat_history:
            for i, msg in enumerate(chat_history[-3:]):  # Show last 3 messages
                print(f"  {i+1}. User: {msg.get('user', '')[:50]}...")
                print(f"     Aara: {msg.get('Aara', '')[:50]}...")
        
        # Use LLM to determine intent and next step
        prompt = f"""
        User input: {user_input}
        Chat history: {chat_history}
        
        Analyze the user's intent. Is this about:
        1. Skincare (skin type, routine, products)
        2. Health advice (periods, PCOS, symptoms)
        3. Need for web search (latest information, research)
        4. Product suggestions (suggest products, recommend items, based on this)
        5. General query that needs rule checking
        
        Respond with just the category number.
        """
        
        try:
            intent_response = llm.invoke(prompt)
            intent = intent_response.content if hasattr(intent_response, 'content') else str(intent_response)
        except Exception as e:
            print(f"Error in reasoning: {e}")
            intent = "5"  # Default to rule engine
        
        # Add reasoning to intermediate steps
        state['intermediate_steps'].append({'reasoning': intent})
        
        # Enhanced routing logic with product suggestion detection
        user_input_lower = user_input.lower()
        
        # Check for explicit product requests first
        product_keywords = [
            'suggest product', 'recommend product', 'suggest some product', 
            'product suggestion', 'product recommendation', 'based on this',
            'show me product', 'what product', 'which product', 'product for',
            'suggest something', 'recommend something', 'shopping', 'buy'
        ]
        
        if any(keyword in user_input_lower for keyword in product_keywords) or '4' in intent:
            state['next_node'] = 'product_suggestion'
        elif 'skin' in user_input_lower or 'skincare' in user_input_lower or '1' in intent:
            state['next_node'] = 'skincare_tool'
        elif any(word in user_input_lower for word in ['period', 'menstrual', 'pcos', 'health']) or '2' in intent:
            state['next_node'] = 'health_advice_tool'
        elif any(word in user_input_lower for word in ['search', 'latest', 'recent', 'research']) or '3' in intent:
            state['next_node'] = 'search_tool'
        else:
            state['next_node'] = 'rule_engine'
        
        return state
    
    return node 