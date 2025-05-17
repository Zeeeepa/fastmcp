"""Tests for the Codegen Agent MCP Client"""

import json
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from mcp.types import TextContent

from fastmcp import Client


@pytest.mark.anyio
async def test_codegen_agent_client():
    """Test the Codegen Agent MCP Client"""
    from examples.codegen_agent_server import mcp
    
    # Mock the Agent class to avoid actual API calls
    with patch("examples.codegen_agent_server.Agent") as MockAgent:
        # Setup mock agent and task
        mock_task = MagicMock()
        mock_task.status = "completed"
        mock_task.result = "Test result"
        
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = mock_task
        
        MockAgent.return_value = mock_agent_instance
        
        async with Client(mcp) as client:
            # Test listing available tools
            tools = await client.list_tools()
            assert len(tools) == 6
            
            # Test getting available prompt templates
            templates = await client.read_resource("prompts://templates")
            assert len(templates.content) == 6
            
            # Test calling create_pr tool
            result = await client.call_tool(
                "create_pr", 
                {
                    "agent_query": "Create a PR that adds a new feature"
                }
            )
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Test calling create_linear_issues tool
            result = await client.call_tool(
                "create_linear_issues", 
                {
                    "agent_query": "Create a main issue for implementing a new authentication system"
                }
            )
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Test calling analyze_codebase tool
            result = await client.call_tool(
                "analyze_codebase", 
                {
                    "agent_query": "Analyze the codebase for performance bottlenecks"
                }
            )
            assert len(result) == 1
            assert isinstance(result[0], TextContent)


@pytest.mark.anyio
async def test_client_with_different_endpoints():
    """Test the client with different endpoints"""
    from examples.codegen_agent_server import mcp
    
    # Mock the Agent class to avoid actual API calls
    with patch("examples.codegen_agent_server.Agent") as MockAgent:
        # Setup mock agent and task
        mock_task = MagicMock()
        mock_task.status = "completed"
        mock_task.result = "Test result"
        
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = mock_task
        
        MockAgent.return_value = mock_agent_instance
        
        async with Client(mcp) as client:
            # Test calling fix_bug tool
            result = await client.call_tool(
                "fix_bug", 
                {
                    "agent_query": "Fix the bug in the login component"
                }
            )
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Test calling review_pr tool
            result = await client.call_tool(
                "review_pr", 
                {
                    "agent_query": "Review the PR #123"
                }
            )
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Test calling generate_documentation tool
            result = await client.call_tool(
                "generate_documentation", 
                {
                    "agent_query": "Generate documentation for the API"
                }
            )
            assert len(result) == 1
            assert isinstance(result[0], TextContent)


@pytest.mark.anyio
async def test_client_with_custom_credentials():
    """Test the client with custom credentials"""
    from examples.codegen_agent_server import mcp
    
    # Mock the Agent class to avoid actual API calls
    with patch("examples.codegen_agent_server.Agent") as MockAgent:
        # Setup mock agent and task
        mock_task = MagicMock()
        mock_task.status = "completed"
        mock_task.result = "Test result"
        
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = mock_task
        
        MockAgent.return_value = mock_agent_instance
        
        async with Client(mcp) as client:
            # Test calling a tool with custom credentials
            result = await client.call_tool(
                "create_pr", 
                {
                    "agent_query": "Create a PR that adds a new feature",
                    "org_id": "custom-org",
                    "token": "custom-token"
                }
            )
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Verify the agent was created with custom credentials
            MockAgent.assert_called_once_with(org_id="custom-org", token="custom-token")

