import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from tools.skincare import skincare_tool
    from tools.health_advice import health_advice_tool
except ImportError:
    import pytest
    pytest.skip("Tool dependencies not available", allow_module_level=True)

def test_skincare_tool():
    """Test skincare tool with dry skin input."""
    state = {'user_input': 'routine for dry skin', 'intermediate_steps': []}
    result = skincare_tool(state)
    assert 'final_response' in result
    assert 'dry skin' in result['final_response'].lower()
    assert 'tool_used' in str(result['intermediate_steps'])

def test_skincare_tool_oily():
    """Test skincare tool with oily skin input."""
    state = {'user_input': 'I have oily skin', 'intermediate_steps': []}
    result = skincare_tool(state)
    assert 'final_response' in result
    assert 'oily skin' in result['final_response'].lower()

def test_skincare_tool_no_match():
    """Test skincare tool with unclear input."""
    state = {'user_input': 'help me with skincare', 'intermediate_steps': []}
    result = skincare_tool(state)
    assert 'final_response' in result
    assert 'skin type' in result['final_response'].lower()

def test_health_advice_tool():
    """Test health advice tool with period tracking input."""
    state = {'user_input': 'How do I track my period?', 'intermediate_steps': []}
    result = health_advice_tool(state)
    assert 'final_response' in result
    assert 'cycle' in result['final_response'].lower() or 'period' in result['final_response'].lower()

def test_health_advice_tool_pcos():
    """Test health advice tool with PCOS input."""
    state = {'user_input': 'Tell me about PCOS', 'intermediate_steps': []}
    result = health_advice_tool(state)
    assert 'final_response' in result
    assert 'pcos' in result['final_response'].lower()

def test_health_advice_tool_no_match():
    """Test health advice tool with unclear input."""
    state = {'user_input': 'general health question', 'intermediate_steps': []}
    result = health_advice_tool(state)
    assert 'final_response' in result
    assert 'specific' in result['final_response'].lower() 