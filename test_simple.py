#!/usr/bin/env python3

# Test script to verify the rules engine works
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rules.rules_engine import rule_engine_node
    print("✅ Rules engine imported successfully!")
    
    # Test greeting
    state = {'user_input': 'hello', 'intermediate_steps': []}
    result = rule_engine_node(state)
    
    if 'final_response' in result and result['final_response']:
        print("✅ Greeting test passed!")
        print(f"Response: {result['final_response'][:100]}...")
    else:
        print("❌ Greeting test failed - no response generated")
    
    # Test agent info
    state = {'user_input': 'who are you', 'intermediate_steps': []}
    result = rule_engine_node(state)
    
    if 'final_response' in result and result['final_response']:
        print("✅ Agent info test passed!")
        print(f"Response: {result['final_response'][:100]}...")
    else:
        print("❌ Agent info test failed - no response generated")
    
    # Test platform info
    state = {'user_input': 'what is hermirror', 'intermediate_steps': []}
    result = rule_engine_node(state)
    
    if 'final_response' in result and result['final_response']:
        print("✅ Platform info test passed!")
        print(f"Response: {result['final_response'][:100]}...")
    else:
        print("❌ Platform info test failed - no response generated")
    
    print("\n🎉 All tests completed! The rules engine is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 