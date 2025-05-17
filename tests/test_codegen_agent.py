"""Tests for the Codegen Agent MCP Server"""

import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from mcp.types import TextContent

from fastmcp import Client
from examples.codegen_agent import CodegenAgent, CodegenTask, Agent


@pytest.mark.anyio
async def test_codegen_agent_initialization():
    """Test the initialization of the CodegenAgent class"""
    agent = CodegenAgent(org_id="test-org", token="test-token")
    assert agent.org_id == "test-org"
    assert agent.token == "test-token"


@pytest.mark.anyio
async def test_codegen_agent_run():
    """Test the run method of the CodegenAgent class"""
    agent = CodegenAgent(org_id="test-org", token="test-token")
    
    # Test successful execution
    result = await agent.run("Test prompt")
    assert result["status"] == "completed"
    assert "Simulated result for prompt" in result["result"]
    
    # Test error handling
    with patch("asyncio.sleep", AsyncMock()) as mock_sleep:
        with patch.object(CodegenAgent, "run", side_effect=Exception("Test error")):
            agent = CodegenAgent(org_id="test-org", token="test-token")
            with pytest.raises(Exception):
                await agent.run("Test prompt")


@pytest.mark.anyio
async def test_codegen_task():
    """Test the CodegenTask class"""
    task = CodegenTask(task_id="test-task")
    assert task.task_id == "test-task"
    assert task.status == "pending"
    assert task.result is None
    assert task.error is None
    
    # Test refresh method
    task.refresh()
    assert task.status == "running"
    
    task.refresh()
    assert task.status == "completed"
    assert task.result == "Simulated result for task test-task"
    
    # Test string representation
    assert str(task) == "CodegenTask(id=test-task, status=completed)"


@pytest.mark.anyio
async def test_agent_class():
    """Test the Agent class"""
    agent = Agent(org_id="test-org", token="test-token")
    assert agent.org_id == "test-org"
    assert agent.token == "test-token"
    
    # Test run method
    task = agent.run("Test prompt")
    assert isinstance(task, CodegenTask)
    assert task.status == "pending"


@pytest.mark.anyio
async def test_codegen_agent_server():
    """Test the Codegen Agent MCP Server"""
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
            tool_names = [tool.name for tool in tools]
            
            # Verify all 6 tools are available
            assert "create_pr" in tool_names
            assert "create_linear_issues" in tool_names
            assert "analyze_codebase" in tool_names
            assert "fix_bug" in tool_names
            assert "review_pr" in tool_names
            assert "generate_documentation" in tool_names
            
            # Test calling a tool
            result = await client.call_tool(
                "create_pr", 
                {
                    "agent_query": "Create a PR that adds a new feature"
                }
            )
            
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Verify the agent was called with the correct parameters
            MockAgent.assert_called_once()
            assert mock_agent_instance.run.called


@pytest.mark.anyio
async def test_prompt_templates_resource():
    """Test the prompt templates resource"""
    from examples.codegen_agent_server import mcp, PROMPT_TEMPLATES
    
    async with Client(mcp) as client:
        # Test getting all templates
        templates = await client.read_resource("prompts://templates")
        assert templates.content == PROMPT_TEMPLATES
        
        # Test getting a specific template
        template = await client.read_resource("prompts://templates/create_pr")
        assert template.content == PROMPT_TEMPLATES["create_pr"]
        
        # Test getting a non-existent template
        with pytest.raises(Exception):
            await client.read_resource("prompts://templates/non_existent")


@pytest.mark.anyio
async def test_error_handling():
    """Test error handling in the Codegen Agent MCP Server"""
    from examples.codegen_agent_server import mcp
    
    # Mock the Agent class to simulate errors
    with patch("examples.codegen_agent_server.Agent") as MockAgent:
        # Setup mock agent and task for error scenario
        mock_task = MagicMock()
        mock_task.status = "error"
        mock_task.error = "Test error"
        
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = mock_task
        
        MockAgent.return_value = mock_agent_instance
        
        async with Client(mcp) as client:
            # Test calling a tool that results in an error
            result = await client.call_tool(
                "create_pr", 
                {
                    "agent_query": "Create a PR that adds a new feature"
                }
            )
            
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            assert "error" in result[0].text.lower()


@pytest.mark.anyio
async def test_custom_credentials():
    """Test using custom credentials"""
    from examples.codegen_agent_server import mcp
    
    # Mock the Agent class
    with patch("examples.codegen_agent_server.Agent") as MockAgent:
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
            
            # Verify the agent was created with custom credentials
            MockAgent.assert_called_once_with(org_id="custom-org", token="custom-token")

