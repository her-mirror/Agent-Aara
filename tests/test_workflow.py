import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

try:
    from agent.workflow import run_workflow
except ImportError:
    # Skip tests if dependencies are not available
    import pytest
    pytest.skip("Workflow dependencies not available", allow_module_level=True)

def test_health_query():
    """Test that health queries return appropriate responses with disclaimers."""
    try:
        response = run_workflow('I have missed my period', [])
        assert isinstance(response, str)
        assert len(response) > 0
        assert 'consult a doctor' in response.lower()
    except Exception as e:
        # Skip test if API keys are not configured
        if "OPENAI_API_KEY" in str(e):
            import pytest
            pytest.skip("OpenAI API key not configured")
        else:
            raise

def test_skincare_query():
    """Test that skincare queries return appropriate responses."""
    try:
        response = run_workflow('What is a good routine for oily skin?', [])
        assert isinstance(response, str)
        assert len(response) > 0
        assert 'consult a doctor' in response.lower()
    except Exception as e:
        # Skip test if API keys are not configured
        if "OPENAI_API_KEY" in str(e):
            import pytest
            pytest.skip("OpenAI API key not configured")
        else:
            raise

def test_empty_input():
    """Test handling of empty input."""
    try:
        response = run_workflow('', [])
        assert isinstance(response, str)
        assert len(response) > 0
    except Exception as e:
        if "OPENAI_API_KEY" in str(e):
            import pytest
            pytest.skip("OpenAI API key not configured")
        else:
            raise 