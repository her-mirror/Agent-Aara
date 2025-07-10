import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

client = TavilyClient(api_key=TAVILY_API_KEY)

def search_tool(state):
    user_input = state['user_input']
    # Use Tavily to search the web
    try:
        result = client.search(user_input)
        state['final_response'] = result['answer']
    except Exception as e:
        state['final_response'] = f"Sorry, I couldn't fetch real-time data right now. ({e})"
    return state 