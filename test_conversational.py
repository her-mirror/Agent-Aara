#!/usr/bin/env python3
"""
Test script to demonstrate the new conversational responses
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agent.workflow import create_agent_workflow

def test_conversational_responses():
    """Test the new conversational responses"""
    
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please add your OpenAI API key to the .env file")
        return
    
    print("🌸 Testing New Conversational Responses")
    print("=" * 50)
    
    # Create the agent workflow
    try:
        workflow = create_agent_workflow()
        print("✅ Agent workflow created successfully")
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        return
    
    # Test cases for conversational responses
    test_cases = [
        {
            "input": "I had a break up today, now I want him to be back in my life",
            "description": "Breakup with desire to get back together - should address this directly"
        },
        {
            "input": "I had a fight with my boyfriend",
            "description": "Relationship issue - should be empathetic and offer support"
        },
        {
            "input": "I'm feeling really down today",
            "description": "Emotional support - should be caring and offer specific help"
        },
        {
            "input": "I'm stressed about work",
            "description": "Stress/anxiety - should be supportive and offer practical help"
        },
        {
            "input": "My skin has been breaking out a lot lately",
            "description": "Skincare concern - should be empathetic and offer specific solutions"
        },
        {
            "input": "I'm having trouble sleeping",
            "description": "Health concern - should be supportive and offer practical advice"
        },
        {
            "input": "Hello!",
            "description": "Simple greeting - should be warm and natural"
        }
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} conversational scenarios...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        print(f"User: {test_case['input']}")
        
        try:
            # Run the workflow
            result = workflow.invoke({
                "user_input": test_case['input'],
                "chat_history": []
            })
            
            # Get the response
            response = result.get('final_response', 'No response generated')
            print(f"Aara: {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)
    
    print("\n🎯 Test Summary:")
    print("The new conversational responses should:")
    print("✅ Sound more natural and personal")
    print("✅ Show genuine empathy and care")
    print("✅ Address what was specifically asked about")
    print("✅ Offer relevant help based on the actual concern")
    print("✅ Feel like talking to a real friend")
    print("✅ Cover all aspects of life (relationships, emotions, health, etc.)")
    print("✅ Not sound robotic or overly formal")
    print("✅ Not change topics to unrelated subjects")

if __name__ == "__main__":
    test_conversational_responses() 