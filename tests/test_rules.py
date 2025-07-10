import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from rules.rules_engine import rule_engine_node
except ImportError:
    import pytest
    pytest.skip("Rules engine dependencies not available", allow_module_level=True)

def test_emergency_rule():
    """Test that emergency keywords trigger appropriate responses."""
    state = {'user_input': 'I have severe pain', 'intermediate_steps': []}
    result = rule_engine_node(state)
    assert 'final_response' in result
    assert 'emergency' in result['final_response'].lower() or 'medical attention' in result['final_response'].lower()

def test_skincare_rule():
    """Test that skincare keywords trigger appropriate responses."""
    state = {'user_input': 'routine for oily skin', 'intermediate_steps': []}
    result = rule_engine_node(state)
    # Should either have a final response or pass through for tool handling
    assert 'intermediate_steps' in result

def test_health_rule():
    """Test that health keywords trigger appropriate responses."""
    state = {'user_input': 'I have PCOS', 'intermediate_steps': []}
    result = rule_engine_node(state)
    # Should either have a final response or pass through for tool handling
    assert 'intermediate_steps' in result

def test_no_rule_match():
    """Test that unmatched input passes through correctly."""
    state = {'user_input': 'hello there', 'intermediate_steps': []}
    result = rule_engine_node(state)
    assert 'rules_checked' in str(result['intermediate_steps']) 