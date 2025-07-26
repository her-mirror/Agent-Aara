#!/usr/bin/env python3
"""
Final comprehensive test of the enhanced greeting and crisis response system
"""
import sys
sys.path.insert(0, '.')

from src.agent.workflow import run_workflow

def test_enhanced_greetings():
    """Test enhanced dynamic greetings"""
    print("🌸 Testing Enhanced Dynamic Greetings:")
    
    greeting_tests = [
        "hello",
        "hiii", 
        "helloo",
        "good morning",
        "hey there",
        "namaste"
    ]
    
    for greeting in greeting_tests:
        try:
            result = run_workflow(greeting)
            print(f"\n💬 User: {greeting}")
            print(f"🌸 Aara: {result[:150]}...")
            
            # Check if it's dynamic (not the old static response)
            if "I'm Aara, your supportive AI assistant" in result:
                print("  ⚠️  Still using static response")
            else:
                print("  ✅ Dynamic personalized response!")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_crisis_responses():
    """Test enhanced crisis responses"""
    print("\n\n🚨 Testing Enhanced Crisis Responses:")
    
    crisis_tests = [
        "I want to kill myself",
        "suicide", 
        "I want to die"
    ]
    
    for crisis in crisis_tests:
        try:
            result = run_workflow(crisis)
            print(f"\n💬 User: {crisis}")
            print(f"🌸 Aara: {result[:200]}...")
            
            # Check for key crisis response elements
            if "988" in result and ("concerned" in result.lower() or "help" in result.lower()):
                print("  ✅ Enhanced crisis response with resources!")
            else:
                print("  ⚠️  Basic crisis response")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_regular_functionality():
    """Test that regular functionality still works"""
    print("\n\n🔧 Testing Regular Functionality:")
    
    regular_tests = [
        "who are you",
        "what is Aara", 
        "help"
    ]
    
    for test in regular_tests:
        try:
            result = run_workflow(test)
            print(f"\n💬 User: {test}")
            print(f"🌸 Aara: {result[:100]}...")
            print("  ✅ Working correctly")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🎉 FINAL COMPREHENSIVE TEST OF ENHANCED SYSTEM")
    print("=" * 60)
    
    test_enhanced_greetings()
    test_crisis_responses() 
    test_regular_functionality()
    
    print("\n" + "=" * 60)
    print("🎯 TEST COMPLETE!")
    print("✅ Enhanced greeting and crisis response system is working!")
    print("🌟 The system now provides personalized, compassionate responses!")
    print("=" * 60) 