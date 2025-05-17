"""Integration tests for the Codegen Agent MCP Server"""

import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from mcp.types import TextContent

from fastmcp import Client, FastMCP
from examples.codegen_agent import CodegenAgent, CodegenTask, Agent


@pytest.mark.anyio
async def test_server_initialization():
    """Test the initialization of the Codegen Agent MCP Server"""
    from examples.codegen_agent_server import mcp
    
    # Verify server properties
    assert isinstance(mcp, FastMCP)
    assert mcp.name == "Codegen Agent Server"
    
    # Verify environment variables are used
    with patch.dict(os.environ, {"CODEGEN_ORG_ID": "env-org", "CODEGEN_TOKEN": "env-token"}):
        # Reload the module to pick up the new environment variables
        import importlib
        import examples.codegen_agent_server
        importlib.reload(examples.codegen_agent_server)
        
        # Verify the environment variables are used
        assert examples.codegen_agent_server.DEFAULT_ORG_ID == "env-org"
        assert examples.codegen_agent_server.DEFAULT_TOKEN == "env-token"


@pytest.mark.anyio
async def test_prompt_templates_configuration():
    """Test the prompt templates configuration"""
    from examples.codegen_agent_server import PROMPT_TEMPLATES
    
    # Verify all required templates are defined
    assert "create_pr" in PROMPT_TEMPLATES
    assert "create_linear_issues" in PROMPT_TEMPLATES
    assert "analyze_codebase" in PROMPT_TEMPLATES
    assert "fix_bug" in PROMPT_TEMPLATES
    assert "review_pr" in PROMPT_TEMPLATES
    assert "generate_documentation" in PROMPT_TEMPLATES
    
    # Verify template format
    for template_name, template in PROMPT_TEMPLATES.items():
        assert "{agent_query}" in template
        assert template.strip() != ""


@pytest.mark.anyio
async def test_run_codegen_agent_function():
    """Test the run_codegen_agent function"""
    from examples.codegen_agent_server import run_codegen_agent, PROMPT_TEMPLATES
    
    # Create a mock context
    mock_ctx = MagicMock()
    mock_ctx.info = AsyncMock()
    mock_ctx.error = AsyncMock()
    
    # Mock the Agent class
    with patch("examples.codegen_agent_server.Agent") as MockAgent:
        # Setup mock agent and task for successful execution
        mock_task = MagicMock()
        mock_task.status = "completed"
        mock_task.result = "Test result"
        
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = mock_task
        
        MockAgent.return_value = mock_agent_instance
        
        # Test successful execution
        result = await run_codegen_agent(
            "create_pr",
            "Create a PR that adds a new feature",
            mock_ctx,
            "test-org",
            "test-token"
        )
        
        # Verify the result
        assert result["status"] == "completed"
        assert result["result"] == "Test result"
        
        # Verify the agent was created with the correct parameters
        MockAgent.assert_called_once_with(org_id="test-org", token="test-token")
        
        # Verify the agent was called with the correct prompt
        expected_prompt = PROMPT_TEMPLATES["create_pr"].format(
            agent_query="Create a PR that adds a new feature"
        )
        mock_agent_instance.run.assert_called_once_with(expected_prompt)
        
        # Verify context logging
        assert mock_ctx.info.called
        
        # Reset mocks
        MockAgent.reset_mock()
        mock_ctx.reset_mock()
        
        # Setup mock agent and task for error scenario
        mock_task = MagicMock()
        mock_task.status = "error"
        mock_task.error = "Test error"
        
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = mock_task
        
        MockAgent.return_value = mock_agent_instance
        
        # Test error scenario
        result = await run_codegen_agent(
            "create_pr",
            "Create a PR that adds a new feature",
            mock_ctx,
            "test-org",
            "test-token"
        )
        
        # Verify the result
        assert result["status"] == "error"
        assert result["error"] == "Test error"
        
        # Verify error logging
        assert mock_ctx.error.called
        
        # Reset mocks
        MockAgent.reset_mock()
        mock_ctx.reset_mock()
        
        # Test exception handling
        mock_agent_instance.run.side_effect = Exception("Test exception")
        
        # Test exception scenario
        result = await run_codegen_agent(
            "create_pr",
            "Create a PR that adds a new feature",
            mock_ctx,
            "test-org",
            "test-token"
        )
        
        # Verify the result
        assert result["status"] == "error"
        assert result["error"] == "Test exception"
        
        # Verify error logging
        assert mock_ctx.error.called


@pytest.mark.anyio
async def test_tool_endpoints():
    """Test all tool endpoints"""
    from examples.codegen_agent_server import mcp
    
    # Mock the Agent class
    with patch("examples.codegen_agent_server.Agent") as MockAgent:
        # Setup mock agent and task
        mock_task = MagicMock()
        mock_task.status = "completed"
        mock_task.result = "Test result"
        
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = mock_task
        
        MockAgent.return_value = mock_agent_instance
        
        async with Client(mcp) as client:
            # Test all endpoints
            endpoints = [
                "create_pr",
                "create_linear_issues",
                "analyze_codebase",
                "fix_bug",
                "review_pr",
                "generate_documentation"
            ]
            
            for endpoint in endpoints:
                # Reset mock
                MockAgent.reset_mock()
                
                # Call the endpoint
                result = await client.call_tool(
                    endpoint, 
                    {
                        "agent_query": f"Test query for {endpoint}"
                    }
                )
                
                # Verify the result
                assert len(result) == 1
                assert isinstance(result[0], TextContent)
                
                # Verify the agent was created
                assert MockAgent.called
                
                # Verify the agent was called with the correct prompt template
                from examples.codegen_agent_server import PROMPT_TEMPLATES
                expected_prompt = PROMPT_TEMPLATES[endpoint].format(
                    agent_query=f"Test query for {endpoint}"
                )
                mock_agent_instance.run.assert_called_once_with(expected_prompt)

