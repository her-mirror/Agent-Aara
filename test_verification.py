#!/usr/bin/env python3
"""
Test script to verify the response verification system
"""
import sys
import os
sys.path.insert(0, '.')

try:
    from src.agent.workflow import run_workflow
    print("✅ Workflow imported successfully")
    
    # Test cases that should trigger verification improvements
    test_cases = [
        "how can i know about my skin type",
        "i dont my skin type",
        "i don't know my skin type",
        "how to find out my skin type",
        "what is my skin type",
        "help me determine my skin type",
    ]
    
    print("\n🔍 Testing Verification System...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: '{test_case}'")
        print("-" * 40)
        
        try:
            response = run_workflow(test_case)
            print(f"Response: {response[:100]}...")
            
            # Check if response is appropriate
            if ("specify your skin type" in response.lower() or 
                "please specify your skin type" in response.lower()):
                print("❌ FAILED: Still asking to specify skin type")
            elif ("determine your skin type" in response.lower() or 
                  "help you figure" in response.lower() or
                  "wash test" in response.lower()):
                print("✅ PASSED: Providing determination guidance")
            else:
                print("⚠️  UNCLEAR: Response unclear")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print()
    
    print("\n🎯 Verification Test Complete!")
    print("The verification system should improve responses that don't match the user's intent.")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc() 