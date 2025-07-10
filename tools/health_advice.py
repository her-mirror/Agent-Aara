from typing import Dict, Any

def health_advice_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """Tool that provides basic health advice for women's health topics."""
    user_input = state['user_input'].lower()
    
    # Define health topics and advice
    health_topics = {
        'period': "To track your menstrual cycle, note the start and end dates each month. A typical cycle is 21-35 days. Regular tracking helps you understand your body's patterns and identify any irregularities.",
        'menstrual': "Menstrual cycles vary from person to person. Normal cycles are 21-35 days long. If you experience severe pain, very heavy bleeding, or irregular cycles, it's important to discuss this with a healthcare provider.",
        'pcos': "PCOS (Polycystic Ovary Syndrome) is a common hormonal condition. Symptoms may include irregular periods, excess hair growth, acne, and weight gain. Management often includes lifestyle changes, medication, and regular monitoring.",
        'cycle': "Cycle tracking helps you understand your body's patterns. You can use a calendar, app, or journal to track your period dates, symptoms, and mood changes. This information is valuable for healthcare discussions.",
        'cramps': "Menstrual cramps are common and can be managed with heat therapy, gentle exercise, over-the-counter pain relievers, and relaxation techniques. Severe cramps that interfere with daily activities should be evaluated by a doctor.",
        'irregular': "Irregular periods can be caused by stress, hormonal changes, weight fluctuations, or underlying conditions. If your periods are consistently irregular, it's worth discussing with a healthcare provider.",
        'hormones': "Hormonal changes throughout your cycle are normal and can affect mood, energy, and physical symptoms. Understanding these patterns can help you better manage your health and wellbeing."
    }
    
    # Check for health topics in user input
    for topic, advice in health_topics.items():
        if topic in user_input:
            state['final_response'] = advice
            state['intermediate_steps'].append({'tool_used': 'health_advice', 'topic': topic})
            return state
    
    # If no specific topic found, provide general guidance
    state['final_response'] = "I can help with women's health topics like menstrual cycles, PCOS, period tracking, and general wellness. Could you please be more specific about what you'd like to know?"
    state['intermediate_steps'].append({'tool_used': 'health_advice', 'action': 'clarification_requested'})
    
    return state 