from rules.rules_engine import rule_engine_node

# Test greeting
state = {'user_input': 'hello', 'intermediate_steps': []}
result = rule_engine_node(state)

print("Result keys:", list(result.keys()))
print("Final response:", result.get('final_response', 'None'))
print("Steps:", result.get('intermediate_steps', [])) 