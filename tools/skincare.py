from typing import Dict, Any

def skincare_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Advanced skincare tool that provides personalized recommendations
    based on skin type, concerns, and user context.
    """
    user_input = state['user_input'].lower()
    chat_history = state.get('chat_history', [])
    
    # Extract context from chat history
    user_context = _extract_user_context(chat_history)
    
    # Define comprehensive skin routines with personalization
    skin_routines = {
        'oily': {
            'basic': "For oily skin: Use a gentle foaming cleanser twice daily, apply an oil-free moisturizer, and use non-comedogenic sunscreen. Avoid heavy creams and over-cleansing.",
            'acne_prone': "For oily, acne-prone skin: Use a salicylic acid cleanser, apply a lightweight, oil-free moisturizer, use non-comedogenic sunscreen, and consider a retinoid treatment (consult a dermatologist first).",
            'sensitive': "For oily, sensitive skin: Use a gentle, fragrance-free cleanser, apply a lightweight, hypoallergenic moisturizer, and use mineral sunscreen."
        },
        'dry': {
            'basic': "For dry skin: Use a hydrating cleanser, apply a rich moisturizer while skin is still damp, and use sunscreen daily. Avoid harsh exfoliants and hot water.",
            'mature': "For dry, mature skin: Use a gentle, hydrating cleanser, apply a rich moisturizer with ceramides or hyaluronic acid, use sunscreen daily, and consider a gentle retinol product.",
            'sensitive': "For dry, sensitive skin: Use a fragrance-free, gentle cleanser, apply a rich, hypoallergenic moisturizer, and use mineral sunscreen."
        },
        'combination': {
            'basic': "For combination skin: Use a gentle cleanser, apply lightweight moisturizer to your whole face, and use different products for oily and dry areas as needed. Use sunscreen daily.",
            'acne_prone': "For combination, acne-prone skin: Use a gentle cleanser with salicylic acid, apply different moisturizers to oily and dry zones, and use non-comedogenic sunscreen."
        },
        'sensitive': {
            'basic': "For sensitive skin: Use fragrance-free, gentle products. Patch test new products first. Use a mild cleanser and hypoallergenic moisturizer.",
            'reactive': "For very sensitive/reactive skin: Use minimal products - gentle cleanser, simple moisturizer, and mineral sunscreen. Introduce new products one at a time."
        },
        'acne': {
            'mild': "For mild acne: Use a gentle cleanser with salicylic acid, apply oil-free moisturizer, use non-comedogenic sunscreen, and avoid over-washing.",
            'moderate': "For moderate acne: Consider a cleanser with benzoyl peroxide or salicylic acid, use oil-free moisturizer, non-comedogenic sunscreen, and consult a dermatologist for treatment options."
        }
    }
    
    # Identify skin type and concerns
    skin_type = _identify_skin_type(user_input)
    concerns = _identify_concerns(user_input)
    
    if skin_type:
        # Get personalized routine based on skin type and concerns
        routine = _get_personalized_routine(skin_type, concerns, skin_routines, user_context)
        
        # Add personalized tips based on context
        personalized_tips = _get_personalized_tips(skin_type, concerns, user_context)
        
        response = routine
        if personalized_tips:
            response += f"\n\n**Additional Tips:** {personalized_tips}"
        
        state['final_response'] = response
        state['intermediate_steps'].append({
            'tool_used': 'skincare', 
            'skin_type': skin_type,
            'concerns': concerns,
            'personalized': True
        })
        return state
    
    # If no specific skin type found, ask intelligent questions
    clarification = _generate_clarification_questions(user_input, user_context)
    state['final_response'] = clarification
    state['intermediate_steps'].append({'tool_used': 'skincare', 'action': 'clarification_requested'})
    
    return state

def _extract_user_context(chat_history):
    """Extract user context from chat history."""
    context = {
        'mentioned_products': [],
        'mentioned_concerns': [],
        'age_mentioned': False,
        'lifestyle_factors': []
    }
    
    for exchange in chat_history:
        if 'user' in exchange:
            user_msg = exchange['user'].lower()
            # Extract mentioned products, concerns, etc.
            if any(word in user_msg for word in ['cleanser', 'moisturizer', 'serum', 'sunscreen']):
                context['mentioned_products'].append(user_msg)
            if any(word in user_msg for word in ['acne', 'wrinkles', 'dark spots', 'redness']):
                context['mentioned_concerns'].append(user_msg)
    
    return context

def _identify_skin_type(user_input):
    """Identify skin type from user input."""
    skin_types = ['oily', 'dry', 'combination', 'sensitive', 'acne']
    for skin_type in skin_types:
        if skin_type in user_input:
            return skin_type
    return None

def _identify_concerns(user_input):
    """Identify skin concerns from user input."""
    concerns = []
    concern_keywords = {
        'acne': ['acne', 'breakouts', 'pimples', 'spots'],
        'aging': ['wrinkles', 'fine lines', 'aging', 'mature'],
        'sensitivity': ['sensitive', 'reactive', 'irritation'],
        'pigmentation': ['dark spots', 'pigmentation', 'melasma']
    }
    
    for concern, keywords in concern_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            concerns.append(concern)
    
    return concerns

def _get_personalized_routine(skin_type, concerns, routines, context):
    """Get personalized routine based on skin type and concerns."""
    if skin_type not in routines:
        return routines.get('sensitive', {}).get('basic', '')
    
    skin_routines = routines[skin_type]
    
    # Choose routine based on concerns
    if 'acne' in concerns and 'acne_prone' in skin_routines:
        return skin_routines['acne_prone']
    elif 'sensitivity' in concerns and 'sensitive' in skin_routines:
        return skin_routines['sensitive']
    elif 'aging' in concerns and 'mature' in skin_routines:
        return skin_routines['mature']
    else:
        return skin_routines.get('basic', '')

def _get_personalized_tips(skin_type, concerns, context):
    """Generate personalized tips based on user profile."""
    tips = []
    
    if 'acne' in concerns:
        tips.append("Change pillowcases frequently and avoid touching your face.")
    
    if skin_type == 'dry':
        tips.append("Use a humidifier in dry environments and drink plenty of water.")
    
    if 'aging' in concerns:
        tips.append("Consistency is key - use products regularly for best results.")
    
    return " ".join(tips)

def _generate_clarification_questions(user_input, context):
    """Generate intelligent clarification questions."""
    if 'routine' in user_input:
        return "To recommend the best skincare routine, could you tell me: What's your skin type (oily, dry, combination, or sensitive)? Do you have any specific concerns like acne, aging, or sensitivity?"
    
    return "To provide the best skincare advice, could you please specify your skin type? For example: oily, dry, combination, sensitive, or acne-prone skin. Also, let me know if you have any specific concerns!" 