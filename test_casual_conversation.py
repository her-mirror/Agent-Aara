#!/usr/bin/env python3
"""
Test script for casual conversation handling
"""
import sys
import os
sys.path.insert(0, '.')

try:
    from src.agent.workflow import run_workflow
    print("✅ Workflow imported successfully")
    
    # Test cases for casual conversations and edge cases
    test_cases = [
        # Casual greetings
        "hii what are you doing",
        "how are you",
        "okay",
        "thanks",
        "bye",
        
        # Previous problematic cases
        "how can i know about my skin type",
        "i dont my skin type",
        
        # Irrelevant questions
        "what's the weather like",
        "tell me a joke",
        "what's 2+2",
        
        # Edge cases
        "hello",
        "help",
        "I don't know"
    ]
    
    print("\n🗣️  Testing Casual Conversation Handling...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: '{test_case}'")
        print("-" * 40)
        
        try:
            response = run_workflow(test_case)
            print(f"Response: {response[:150]}...")
            
            # Check response quality
            if "error" in response.lower() or "rule_engine" in response.lower():
                print("❌ FAILED: System error occurred")
            elif any(word in response.lower() for word in ["help", "skincare", "health", "wellness"]):
                print("✅ PASSED: Appropriate response with health/skincare context")
            elif test_case in ["thanks", "bye", "okay"] and any(word in response.lower() for word in ["welcome", "care", "help"]):
                print("✅ PASSED: Good casual response")
            else:
                print("⚠️  UNCLEAR: Review response quality")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print()
    
    print("\n🎯 Casual Conversation Test Complete!")
    print("All casual conversations should be handled gracefully with redirects to health topics.")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc() 