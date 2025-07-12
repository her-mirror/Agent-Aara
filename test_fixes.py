#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from rules.rules_engine import is_greeting, is_crisis_situation, rule_engine_node

# Test improved greeting detection
print('Testing improved greeting detection:')
test_greetings = ['hello', 'hiii', 'helloo', 'heyy', 'good morning']
for greeting in test_greetings:
    result = is_greeting(greeting)
    print(f'  {greeting}: {result}')

print('\nTesting crisis detection:')
test_crisis = ['I want to kill myself', 'suicide', 'I want to die']
for crisis in test_crisis:
    result = is_crisis_situation(crisis)
    print(f'  {crisis}: {result}')

print('\nTesting rule engine routing:')
# Test greeting routing
state = {'user_input': 'hiii', 'intermediate_steps': []}
result = rule_engine_node(state)
print(f'  hiii -> use_llm: {result.get("use_llm")}, response_type: {result.get("response_type")}')

# Test crisis routing
state = {'user_input': 'I want to kill myself', 'intermediate_steps': []}
result = rule_engine_node(state)
print(f'  crisis -> use_llm: {result.get("use_llm")}, response_type: {result.get("response_type")}')
print(f'  crisis -> final_response: {bool(result.get("final_response"))}') 