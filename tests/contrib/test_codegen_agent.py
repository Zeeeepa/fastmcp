"""
Tests for the Codegen Agent MCP Server.
"""

import pytest
from fastmcp.contrib.codegen_agent import CodegenAgentServer, Agent, CodegenTask

@pytest.fixture
def server():
    """Create a Codegen Agent MCP Server for testing."""
    server = CodegenAgentServer(
        org_id="test-org-id",
        api_token="test-api-token",
        name="Test Codegen Agent Server"
    )
    server.configure_tools()
    return server

def test_server_initialization(server):
    """Test that the server initializes correctly."""
    assert server.name == "Test Codegen Agent Server"
    assert isinstance(server.agent, Agent)
    assert server.agent.org_id == "test-org-id"
    assert server.agent.token == "test-api-token"

def test_prompt_registration(server):
    """Test that prompts are registered correctly."""
    prompts = server.prompts.list()
    prompt_names = [prompt.name for prompt in prompts]
    
    assert "code_generation" in prompt_names
    assert "code_explanation" in prompt_names
    assert "code_refactoring" in prompt_names
    assert "bug_fixing" in prompt_names
    assert "code_review" in prompt_names
    assert "documentation" in prompt_names

def test_tool_registration(server):
    """Test that tools are registered correctly."""
    tools = server.tools.list()
    tool_names = [tool.name for tool in tools]
    
    assert "generate_code" in tool_names
    assert "explain_code" in tool_names
    assert "refactor_code" in tool_names
    assert "fix_bug" in tool_names
    assert "review_code" in tool_names
    assert "generate_documentation" in tool_names

def test_resource_registration(server):
    """Test that resources are registered correctly."""
    resources = server.resources.list()
    resource_uris = [resource.uri for resource in resources]
    
    assert "codegen://prompts" in resource_uris
    assert any(uri.startswith("codegen://prompts/") for uri in resource_uris)

@pytest.mark.asyncio
async def test_codegen_task():
    """Test the CodegenTask class."""
    task = CodegenTask("test-task-id")
    
    assert task.task_id == "test-task-id"
    assert task.status == "pending"
    assert task.result is None
    assert task.error is None
    
    task.refresh()
    assert task.status == "running"
    
    task.refresh()
    assert task.status == "completed"
    assert task.result == "Task test-task-id completed successfully"

