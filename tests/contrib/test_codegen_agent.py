"""
Tests for the Codegen Agent API wrapper.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from fastmcp.contrib.codegen_agent import CodegenAgent, Agent, CodegenTask, TaskStatus, CodegenApiError

class TestCodegenTask:
    """
    Tests for the CodegenTask class.
    """
    
    def test_init(self):
        """
        Test initialization of CodegenTask.
        """
        task = CodegenTask("test_task_id")
        assert task.task_id == "test_task_id"
        assert task.status == TaskStatus.PENDING
        assert task.result is None
        assert task.error is None
    
    @pytest.mark.asyncio
    async def test_refresh_mock(self):
        """
        Test refreshing a task in mock mode.
        """
        task = CodegenTask("test_task_id")
        await task.refresh()
        assert task.status == TaskStatus.RUNNING
        
        await task.refresh()
        assert task.status == TaskStatus.COMPLETED
        assert task.result is not None
    
    def test_refresh_sync_mock(self):
        """
        Test refreshing a task synchronously in mock mode.
        """
        task = CodegenTask("test_task_id")
        task.refresh_sync()
        assert task.status == TaskStatus.RUNNING
        
        task.refresh_sync()
        assert task.status == TaskStatus.COMPLETED
        assert task.result is not None
    
    def test_str(self):
        """
        Test string representation of CodegenTask.
        """
        task = CodegenTask("test_task_id")
        assert str(task) == "CodegenTask(id=test_task_id, status=pending)"


class TestAgent:
    """
    Tests for the Agent class.
    """
    
    def test_init(self):
        """
        Test initialization of Agent.
        """
        agent = Agent("test_org_id", "test_token")
        assert agent.org_id == "test_org_id"
        assert agent.token == "test_token"
        assert agent.mock_mode is False
    
    def test_run_mock(self):
        """
        Test running an agent in mock mode.
        """
        agent = Agent("test_org_id", "test_token", mock_mode=True)
        task = agent.run("Test prompt")
        assert isinstance(task, CodegenTask)
        assert task.task_id.startswith("mock_task_")
    
    @pytest.mark.asyncio
    async def test_run_async_mock(self):
        """
        Test running an agent asynchronously in mock mode.
        """
        agent = Agent("test_org_id", "test_token", mock_mode=True)
        task = await agent.run_async("Test prompt")
        assert isinstance(task, CodegenTask)
        assert task.task_id.startswith("mock_task_")
    
    @patch("httpx.Client")
    def test_run_api(self, mock_client):
        """
        Test running an agent via the API.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"task_id": "api_task_123"}
        
        # Mock the client
        mock_client_instance = MagicMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        # Run the agent
        agent = Agent("test_org_id", "test_token")
        task = agent.run("Test prompt")
        
        # Verify the result
        assert isinstance(task, CodegenTask)
        assert task.task_id == "api_task_123"
        
        # Verify the API call
        mock_client_instance.post.assert_called_once()
        args, kwargs = mock_client_instance.post.call_args
        assert args[0].endswith("/agents/run")
        assert kwargs["json"]["organization_id"] == "test_org_id"
        assert kwargs["json"]["prompt"] == "Test prompt"
    
    @patch("httpx.Client")
    def test_run_api_error(self, mock_client):
        """
        Test error handling when running an agent via the API.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        
        # Mock the client
        mock_client_instance = MagicMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        # Run the agent and expect an error
        agent = Agent("test_org_id", "test_token")
        with pytest.raises(CodegenApiError) as excinfo:
            agent.run("Test prompt")
        
        # Verify the error
        assert "Error creating task: 400" in str(excinfo.value)
    
    @patch("httpx.Client")
    def test_refresh_task_sync(self, mock_client):
        """
        Test refreshing a task synchronously via the API.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "completed",
            "result": "Test result"
        }
        
        # Mock the client
        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        # Create an agent and task
        agent = Agent("test_org_id", "test_token")
        task = CodegenTask("test_task_id", agent=agent)
        
        # Refresh the task
        agent.refresh_task_sync(task)
        
        # Verify the result
        assert task.status == "completed"
        assert task.result == "Test result"
        
        # Verify the API call
        mock_client_instance.get.assert_called_once()
        args, kwargs = mock_client_instance.get.call_args
        assert args[0].endswith("/agents/tasks/test_task_id")


class TestCodegenAgent:
    """
    Tests for the CodegenAgent class.
    """
    
    def test_init(self):
        """
        Test initialization of CodegenAgent.
        """
        agent = CodegenAgent("test_org_id", "test_token")
        assert agent.org_id == "test_org_id"
        assert agent.token == "test_token"
        assert agent.mock_mode is False
    
    @pytest.mark.asyncio
    async def test_run_mock(self):
        """
        Test running a Codegen Agent in mock mode.
        """
        agent = CodegenAgent("test_org_id", "test_token", mock_mode=True)
        result = await agent.run("Test prompt")
        
        assert result["status"] == "completed"
        assert "result" in result
    
    @pytest.mark.asyncio
    async def test_run_error(self):
        """
        Test error handling when running a Codegen Agent.
        """
        agent = CodegenAgent("test_org_id", "test_token")
        
        # Mock the Agent.run method to raise an exception
        with patch("fastmcp.contrib.codegen_agent.agent.Agent.run") as mock_run:
            mock_run.side_effect = CodegenApiError("Test error")
            
            result = await agent.run("Test prompt")
            
            assert result["status"] == "error"
            assert "error" in result
            assert "Test error" in result["error"]

