"""Tests for the Codegen Agent MCP Server error handling"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from mcp.types import TextContent

from fastmcp import Client


@pytest.mark.anyio
async def test_agent_error_handling():
    """Test error handling when the agent returns an error"""
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
            
            # Verify the error is properly handled
            text_content = result[0].text
            assert "error" in text_content.lower()
            assert "Test error" in text_content


@pytest.mark.anyio
async def test_agent_exception_handling():
    """Test error handling when the agent raises an exception"""
    from examples.codegen_agent_server import mcp
    
    # Mock the Agent class to simulate exceptions
    with patch("examples.codegen_agent_server.Agent") as MockAgent:
        # Setup mock agent to raise an exception
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.side_effect = Exception("Test exception")
        
        MockAgent.return_value = mock_agent_instance
        
        async with Client(mcp) as client:
            # Test calling a tool that raises an exception
            result = await client.call_tool(
                "create_pr", 
                {
                    "agent_query": "Create a PR that adds a new feature"
                }
            )
            
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Verify the exception is properly handled
            text_content = result[0].text
            assert "error" in text_content.lower()
            assert "Test exception" in text_content


@pytest.mark.anyio
async def test_task_status_polling_error():
    """Test error handling when polling task status"""
    from examples.codegen_agent_server import mcp
    
    # Mock the Agent class and asyncio.sleep
    with patch("examples.codegen_agent_server.Agent") as MockAgent, \
         patch("examples.codegen_agent_server.asyncio.sleep", AsyncMock()) as mock_sleep:
        
        # Setup mock agent and task that transitions to failed status
        mock_task = MagicMock()
        # First status check returns "running"
        # Second status check returns "failed"
        mock_task.status = "running"
        
        def update_status():
            mock_task.status = "failed"
            mock_task.error = "Task failed"
        
        # When refresh is called, update the status
        mock_task.refresh.side_effect = update_status
        
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = mock_task
        
        MockAgent.return_value = mock_agent_instance
        
        async with Client(mcp) as client:
            # Test calling a tool that results in a failed task
            result = await client.call_tool(
                "create_pr", 
                {
                    "agent_query": "Create a PR that adds a new feature"
                }
            )
            
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Verify the error is properly handled
            text_content = result[0].text
            assert "failed" in text_content.lower()
            assert "Task failed" in text_content
            
            # Verify sleep was called (for polling)
            assert mock_sleep.called


@pytest.mark.anyio
async def test_invalid_template_error():
    """Test error handling when an invalid template is specified"""
    from examples.codegen_agent_server import run_codegen_agent
    
    # Create a mock context
    mock_ctx = MagicMock()
    mock_ctx.info = AsyncMock()
    mock_ctx.error = AsyncMock()
    
    # Test with an invalid template name
    with pytest.raises(KeyError):
        await run_codegen_agent(
            "nonexistent_template",
            "Test query",
            mock_ctx,
            "test-org",
            "test-token"
        )


@pytest.mark.anyio
async def test_resource_not_found_error():
    """Test error handling when a resource is not found"""
    from examples.codegen_agent_server import mcp
    
    async with Client(mcp) as client:
        # Test accessing a nonexistent resource
        with pytest.raises(Exception):
            await client.read_resource("prompts://nonexistent")
            
        # Test accessing a nonexistent template
        with pytest.raises(Exception):
            await client.read_resource("prompts://templates/nonexistent")

