#!/usr/bin/env python3
"""
Quick diagnosis script to identify the root cause of the 'rule_engine' error
"""
import sys
import os
sys.path.insert(0, '.')

try:
    # Test 1: Import rules engine directly
    print("🔍 Testing imports...")
    from rules.rules_engine import rule_engine_node, is_greeting, is_crisis_situation
    print("✅ Rules engine imported successfully")
    
    # Test 2: Test greeting detection
    print("\n🔍 Testing greeting detection...")
    test_cases = ['hello', 'hiii', 'helloo', 'good morning']
    for case in test_cases:
        result = is_greeting(case)
        print(f"  {case}: {result}")
    
    # Test 3: Test rule engine directly
    print("\n🔍 Testing rule engine directly...")
    state = {'user_input': 'hello', 'intermediate_steps': []}
    result = rule_engine_node(state)
    print(f"  Result keys: {list(result.keys())}")
    print(f"  use_llm: {result.get('use_llm')}")
    print(f"  response_type: {result.get('response_type')}")
    
    # Test 4: Test workflow imports
    print("\n🔍 Testing workflow imports...")
    try:
        from src.agent.workflow import run_workflow
        print("✅ Workflow imported successfully")
        
        # Test 5: Test workflow with simple input
        print("\n🔍 Testing workflow execution...")
        result = run_workflow("hello")
        print(f"  Result: {result[:100]}...")
        
    except Exception as e:
        print(f"❌ Workflow import/execution failed: {e}")
        import traceback
        traceback.print_exc()
        
    print("\n🎯 Diagnosis complete!")
    
except Exception as e:
    print(f"❌ Error during diagnosis: {e}")
    import traceback
    traceback.print_exc() 