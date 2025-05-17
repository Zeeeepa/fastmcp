"""Tests for the Codegen Agent MCP Server resources"""

import pytest
from unittest.mock import patch, MagicMock
from mcp.types import TextResourceContents

from fastmcp import Client


@pytest.mark.anyio
async def test_templates_resource():
    """Test the templates resource"""
    from examples.codegen_agent_server import mcp, PROMPT_TEMPLATES
    
    async with Client(mcp) as client:
        # Test getting all templates
        result = await client.read_resource("prompts://templates")
        assert isinstance(result, TextResourceContents)
        assert result.content == PROMPT_TEMPLATES
        
        # Verify all templates are available
        assert "create_pr" in result.content
        assert "create_linear_issues" in result.content
        assert "analyze_codebase" in result.content
        assert "fix_bug" in result.content
        assert "review_pr" in result.content
        assert "generate_documentation" in result.content


@pytest.mark.anyio
async def test_individual_template_resources():
    """Test individual template resources"""
    from examples.codegen_agent_server import mcp, PROMPT_TEMPLATES
    
    async with Client(mcp) as client:
        # Test each individual template
        for template_name in PROMPT_TEMPLATES:
            result = await client.read_resource(f"prompts://templates/{template_name}")
            assert isinstance(result, TextResourceContents)
            assert result.content == PROMPT_TEMPLATES[template_name]


@pytest.mark.anyio
async def test_nonexistent_template_resource():
    """Test accessing a nonexistent template resource"""
    from examples.codegen_agent_server import mcp
    
    async with Client(mcp) as client:
        # Test getting a nonexistent template
        with pytest.raises(Exception):
            await client.read_resource("prompts://templates/nonexistent")


@pytest.mark.anyio
async def test_template_resource_validation():
    """Test template resource validation"""
    from examples.codegen_agent_server import mcp, get_prompt_template
    
    # Test with a valid template name
    result = get_prompt_template("create_pr")
    assert isinstance(result, str)
    assert "{agent_query}" in result
    
    # Test with an invalid template name
    with pytest.raises(ValueError):
        get_prompt_template("nonexistent")


@pytest.mark.anyio
async def test_template_resource_content():
    """Test template resource content"""
    from examples.codegen_agent_server import mcp, PROMPT_TEMPLATES
    
    async with Client(mcp) as client:
        # Test that each template contains the required placeholder
        for template_name in PROMPT_TEMPLATES:
            result = await client.read_resource(f"prompts://templates/{template_name}")
            assert "{agent_query}" in result.content
            
            # Test that the template is not empty
            assert result.content.strip() != ""
            
            # Test that the template contains instructions
            assert "Instructions:" in result.content

