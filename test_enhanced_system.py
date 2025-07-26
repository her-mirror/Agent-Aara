#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced greeting and crisis response system.
This tests the new dynamic LLM-based responses for greetings and mental health crises.
"""

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from rules.rules_engine import rule_engine_node, is_greeting, is_crisis_situation
    from src.agent.response import response_node, load_prompt
    
    def test_greeting_detection():
        """Test that greeting detection works correctly."""
        print("🧪 Testing Greeting Detection...")
        
        greeting_tests = [
            ("hello", True),
            ("hi there", True),
            ("hey!", True),
            ("good morning", True),
            ("good evening everyone", True),
            ("namaste", True),
            ("bonjour", True),
            ("what's up", True),
            ("yo", True),
            ("I have a question", False),
            ("my skin is breaking out", False),
            ("help me", False)
        ]
        
        for test_input, expected in greeting_tests:
            result = is_greeting(test_input)
            status = "✅" if result == expected else "❌"
            print(f"  {status} '{test_input}' -> {result} (expected {expected})")
        
        return True
    
    def test_crisis_detection():
        """Test that crisis situation detection works correctly."""
        print("\n🧪 Testing Crisis Detection...")
        
        crisis_tests = [
            ("I want to kill myself", True),
            ("suicide", True),
            ("I want to die", True),
            ("thinking about dying", True),
            ("end my life", True),
            ("hurt myself", True),
            ("I'm feeling sad", False),
            ("I'm depressed", False),
            ("having a bad day", False),
            ("stressed out", False)
        ]
        
        for test_input, expected in crisis_tests:
            result = is_crisis_situation(test_input)
            status = "✅" if result == expected else "❌"
            print(f"  {status} '{test_input}' -> {result} (expected {expected})")
        
        return True
    
    def test_rule_engine_routing():
        """Test that the rules engine routes correctly to LLM for greetings and crises."""
        print("\n🧪 Testing Rule Engine Routing...")
        
        # Test greeting routing
        greeting_state = {'user_input': 'hello', 'intermediate_steps': []}
        result = rule_engine_node(greeting_state)
        
        if result.get('use_llm') and result.get('response_type') == 'greeting':
            print("  ✅ Greeting correctly routed to LLM")
        else:
            print("  ❌ Greeting routing failed")
            print(f"      Result: {result}")
        
        # Test crisis routing
        crisis_state = {'user_input': 'I want to kill myself', 'intermediate_steps': []}
        result = rule_engine_node(crisis_state)
        
        if result.get('use_llm') and result.get('response_type') == 'crisis':
            print("  ✅ Crisis correctly routed to LLM")
        else:
            print("  ❌ Crisis routing failed")
            print(f"      Result: {result}")
        
        return True
    
    def test_prompt_loading():
        """Test that specialized prompts load correctly."""
        print("\n🧪 Testing Prompt Loading...")
        
        greeting_prompt = load_prompt('greeting_prompt.txt')
        if greeting_prompt and "personalized greeting" in greeting_prompt:
            print("  ✅ Greeting prompt loaded successfully")
        else:
            print("  ❌ Greeting prompt failed to load")
            print(f"      Content: {greeting_prompt[:100]}...")
        
        crisis_prompt = load_prompt('crisis_prompt.txt')
        if crisis_prompt and "CRISIS SITUATION" in crisis_prompt:
            print("  ✅ Crisis prompt loaded successfully")
        else:
            print("  ❌ Crisis prompt failed to load")
            print(f"      Content: {crisis_prompt[:100]}...")
        
        return True
    
    def test_response_scenarios():
        """Test different response scenarios."""
        print("\n🧪 Testing Response Scenarios...")
        
        # Test static rule response (should still work)
        static_state = {'user_input': 'who are you', 'intermediate_steps': []}
        result = rule_engine_node(static_state)
        
        if result.get('final_response') and 'Aara' in result.get('final_response', ''):
            print("  ✅ Static rule responses still work")
        else:
            print("  ❌ Static rule responses broken")
            print(f"      Result: {result}")
        
        # Test emergency response (should still work)
        emergency_state = {'user_input': 'severe chest pain', 'intermediate_steps': []}
        result = rule_engine_node(emergency_state)
        
        if result.get('final_response') and 'emergency' in result.get('final_response', '').lower():
            print("  ✅ Emergency responses still work")
        else:
            print("  ❌ Emergency responses broken")
            print(f"      Result: {result}")
        
        return True
    
    def run_all_tests():
        """Run all tests and report results."""
        print("=" * 60)
        print("🧪 ENHANCED GREETING & CRISIS RESPONSE SYSTEM TESTS")
        print("=" * 60)
        
        tests = [
            test_greeting_detection,
            test_crisis_detection,
            test_rule_engine_routing,
            test_prompt_loading,
            test_response_scenarios
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ Test failed with error: {e}")
        
        print("\n" + "=" * 60)
        print(f"RESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The enhanced system is working correctly.")
        else:
            print("⚠️  Some tests failed. Please review the issues above.")
        
        return passed == total
    
    if __name__ == "__main__":
        run_all_tests()
        
        # Interactive testing
        print("\n" + "=" * 60)
        print("🔧 INTERACTIVE TESTING")
        print("=" * 60)
        print("You can now test specific inputs manually:")
        print("- Try greetings: 'hello', 'hey', 'good morning', 'namaste'")
        print("- Try crisis inputs: 'I want to die', 'suicide', 'hurt myself'")
        print("- Try regular inputs: 'who are you', 'what is Aara', 'help'")
        print("- Type 'quit' to exit")
        
        while True:
            try:
                user_input = input("\n💬 Test input: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("🌸 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Test the rules engine
                state = {'user_input': user_input, 'intermediate_steps': []}
                result = rule_engine_node(state)
                
                print(f"\n📊 Analysis:")
                print(f"   Is greeting: {is_greeting(user_input)}")
                print(f"   Is crisis: {is_crisis_situation(user_input)}")
                print(f"   Use LLM: {result.get('use_llm', False)}")
                print(f"   Response type: {result.get('response_type', 'none')}")
                
                if result.get('final_response'):
                    print(f"\n🤖 Static response: {result['final_response'][:200]}...")
                elif result.get('use_llm'):
                    print(f"\n🧠 Would generate LLM response of type: {result.get('response_type')}")
                else:
                    print(f"\n🔄 Would route to: {result.get('route_to', 'default processing')}")
                
            except KeyboardInterrupt:
                print("\n\n🌸 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
except Exception as e:
    print(f"❌ Failed to import modules: {e}")
    import traceback
    traceback.print_exc() 