#!/usr/bin/env python3
"""
Test script for the Product Suggestion feature.
This demonstrates how the product suggestion tool analyzes conversations
and provides relevant affiliate product recommendations.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

from tools.product_suggestion import product_suggestion_tool, ProductSuggestionTool

def test_product_suggestions():
    """Test various scenarios for product suggestions."""
    
    print("🧪 Testing Product Suggestion Feature")
    print("=" * 50)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Oily Skin Routine",
            "user_input": "I have oily skin and keep getting acne. What routine should I follow?",
            "chat_history": [
                {"user": "Hi! I need help with skincare", "ara": "Hello! I'd love to help with your skincare needs."},
                {"user": "I have oily skin and keep getting acne", "ara": "I understand how frustrating that can be."}
            ]
        },
        {
            "name": "PCOS Management",
            "user_input": "I was diagnosed with PCOS and having irregular periods. Any supplements that might help?",
            "chat_history": [
                {"user": "I'm dealing with hormonal issues", "ara": "I'm here to support you through this."}
            ]
        },
        {
            "name": "Dry Skin Issues",
            "user_input": "My skin feels so dry and tight, especially in winter. Need a gentle cleanser recommendation.",
            "chat_history": [
                {"user": "My skin is always dry", "ara": "Dry skin can be challenging to manage."}
            ]
        },
        {
            "name": "Menstrual Cramps",
            "user_input": "I get terrible period cramps every month. What can help with the pain?",
            "chat_history": [
                {"user": "Period pain is awful", "ara": "I understand how difficult period pain can be."}
            ]
        },
        {
            "name": "Emergency Situation (Should NOT suggest products)",
            "user_input": "I'm having severe abdominal pain and heavy bleeding. This is an emergency!",
            "chat_history": []
        },
        {
            "name": "User Explicitly Says No Products",
            "user_input": "I don't want any product recommendations, just advice on skincare routine",
            "chat_history": []
        }
    ]
    
    tool = ProductSuggestionTool()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print("-" * 30)
        print(f"User Input: {test_case['user_input']}")
        
        # Create state
        state = {
            'user_input': test_case['user_input'],
            'chat_history': test_case['chat_history'],
            'final_response': '',
            'intermediate_steps': []
        }
        
        # Run the product suggestion tool
        result = product_suggestion_tool(state)
        
        # Show results
        if result.get('final_response'):
            print(f"\n✅ Product suggestions generated:")
            print(result['final_response'])
        else:
            print(f"\n❌ No product suggestions (as expected for this scenario)")
        
        if result.get('intermediate_steps'):
            for step in result['intermediate_steps']:
                if step.get('tool_used') == 'product_suggestion':
                    print(f"\n📊 Context Analysis:")
                    print(f"   - Products suggested: {step.get('products_suggested', [])}")
                    print(f"   - Reason: {step.get('suggestion_reason', 'N/A')}")
        
        print("\n" + "="*50)

def test_context_analysis():
    """Test the context analysis functionality."""
    print("\n🔍 Testing Context Analysis")
    print("=" * 50)
    
    tool = ProductSuggestionTool()
    
    test_inputs = [
        "I have oily skin with large pores and acne",
        "My dry skin needs hydration, looking for affordable products",
        "PCOS symptoms are getting worse, irregular periods",
        "Need eco-friendly period products, heavy flow"
    ]
    
    for user_input in test_inputs:
        print(f"\nInput: {user_input}")
        context = tool.analyze_conversation_context(user_input, [])
        print(f"Context Analysis:")
        for key, value in context.items():
            if value:  # Only show non-empty values
                print(f"  - {key}: {value}")

def test_product_loading():
    """Test product database loading."""
    print("\n📦 Testing Product Database Loading")
    print("=" * 50)
    
    tool = ProductSuggestionTool()
    products = tool.products
    
    print(f"Total products loaded: {len(products)}")
    
    # Group by category
    categories = {}
    for product in products:
        if product.category not in categories:
            categories[product.category] = []
        categories[product.category].append(product)
    
    for category, products_list in categories.items():
        print(f"\n{category.upper()}:")
        for product in products_list:
            print(f"  - {product.name} ({product.price_range})")

if __name__ == "__main__":
    print("🌸 Ara Health Agent - Product Suggestion Testing")
    print("=" * 60)
    
    try:
        # Test product database loading
        test_product_loading()
        
        # Test context analysis
        test_context_analysis()
        
        # Test full product suggestions
        test_product_suggestions()
        
        print("\n✅ All tests completed!")
        print("\n💡 To use this feature:")
        print("1. Update affiliate links in config/affiliate_links.yaml")
        print("2. Start the agent with: python scripts/run_agent.py")
        print("3. Ask questions about skincare/health concerns")
        print("4. The agent will automatically suggest relevant products!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc() 