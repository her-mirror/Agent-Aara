import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

try:
    from agent.workflow import run_workflow
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this script from the project root directory")
    print("And that all required packages are installed: pip install -r requirements.txt")
    sys.exit(1)

def main():
    print("=" * 50)
    print("🌸 Ara: Women's Health & Skincare AI Agent 🌸")
    print("=" * 50)
    print("Hi! I'm Ara, your supportive AI assistant for women's health and skincare.")
    print("I can help with topics like:")
    print("• Skincare routines for different skin types")
    print("• Menstrual health and cycle tracking")
    print("• PCOS and hormonal health")
    print("• General wellness advice")
    print("\nType 'exit' or 'quit' to end our conversation.")
    print("-" * 50)
    
    chat_history = []
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("\n🌸 Ara: Take care! Remember to prioritize your health and wellbeing. Goodbye! 🌸")
                break
            
            if not user_input:
                print("🌸 Ara: I'm here to help! Please ask me anything about women's health or skincare.")
                continue
            
            print("\n🤔 Ara is thinking...")
            response = run_workflow(user_input, chat_history)
            print(f"\n🌸 Ara: {response}")
            
            # Update chat history
            chat_history.append({'user': user_input, 'ara': response})
            
            # Keep only last 5 exchanges to manage memory
            if len(chat_history) > 5:
                chat_history = chat_history[-5:]
                
        except KeyboardInterrupt:
            print("\n\n🌸 Ara: Goodbye! Take care of yourself! 🌸")
            break
        except Exception as e:
            print(f"\n❌ Sorry, I encountered an error: {e}")
            print("Please try again or type 'exit' to quit.")

if __name__ == '__main__':
    main() 