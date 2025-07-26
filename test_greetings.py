 #!/usr/bin/env python3
"""
Simple test script to demonstrate the new greeting and info functionality.
Run this to see how Aara responds to greetings and questions about herself and HerMirror.
"""

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from rules.rules_engine import rule_engine_node
    
    def test_response(user_input):
        """Test a user input and print the response."""
        print(f"\n🔵 User: {user_input}")
        state = {'user_input': user_input, 'intermediate_steps': []}
        result = rule_engine_node(state)
        
        if 'final_response' in result and result['final_response']:
            print(f"🌸 Aara: {result['final_response']}")
        else:
            print("🔄 No direct response - would be passed to tools/reasoning")
        
        # Show which rule was triggered
        if result['intermediate_steps']:
            last_step = result['intermediate_steps'][-1]
            rule_type = last_step.get('rule_type', 'unknown')
            print(f"📋 Rule triggered: {rule_type}")
    
    print("=" * 60)
    print("🌸 Testing Aara's New Greeting & Info Responses 🌸")
    print("=" * 60)
    
    # Test greetings
    print("\n🎯 TESTING GREETINGS:")
    test_response("hello")
    test_response("hi")
    test_response("hey there")
    test_response("good morning")
    
    # Test agent info
    print("\n🎯 TESTING AGENT INFO:")
    test_response("who are you")
    test_response("what is Aara")
    test_response("what can you do")
    
    # Test platform info
    print("\n🎯 TESTING PLATFORM INFO:")
    test_response("what is hermirror")
    test_response("about hermirror")
    
    # Test help
    print("\n🎯 TESTING HELP:")
    test_response("help")
    
    # Test non-matching input
    print("\n🎯 TESTING NON-MATCHING INPUT:")
    test_response("I have oily skin")
    test_response("tell me about PCOS")
    
    print("\n" + "=" * 60)
    print("✅ Test completed! Aara is ready to greet users and share info!")
    print("=" * 60)

except ImportError as e:
    print(f"❌ Error importing rules engine: {e}")
    print("Make sure you're in the project root directory and rules are set up correctly.")
except Exception as e:
    print(f"❌ Error running tests: {e}")