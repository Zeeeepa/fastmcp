"""
Codegen Agent API Integration Module

This module provides a wrapper around the Codegen Agent API for use with FastMCP.
"""

from typing import Dict, Any, Optional, Union, List
import asyncio
import logging
import os
import json
import time
import uuid
import httpx
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default API endpoint
DEFAULT_API_ENDPOINT = "https://api.codegen.sh/v1"

class TaskStatus(str, Enum):
    """
    Enum representing the possible statuses of a Codegen Agent task.
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ERROR = "error"


class CodegenApiError(Exception):
    """
    Exception raised for errors in the Codegen API.
    """
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class CodegenTask:
    """
    Represents a task executed by the Codegen Agent.
    """
    
    def __init__(
        self, 
        task_id: str, 
        status: str = TaskStatus.PENDING, 
        agent: Optional["Agent"] = None
    ):
        """
        Initialize a Codegen Task.
        
        Args:
            task_id: The task ID
            status: The initial status of the task
            agent: The agent instance that created this task
        """
        self.task_id = task_id
        self.status = status
        self.result = None
        self.error = None
        self._agent = agent
    
    async def refresh(self) -> None:
        """
        Refresh the task status asynchronously.
        
        Raises:
            CodegenApiError: If there's an error refreshing the task status
        """
        if self._agent:
            await self._agent.refresh_task(self)
        else:
            # In mock mode, simulate a status update
            if self.status == TaskStatus.PENDING:
                self.status = TaskStatus.RUNNING
            elif self.status == TaskStatus.RUNNING:
                self.status = TaskStatus.COMPLETED
                self.result = f"Simulated result for task {self.task_id}"
    
    def refresh_sync(self) -> None:
        """
        Refresh the task status synchronously.
        
        Raises:
            CodegenApiError: If there's an error refreshing the task status
        """
        if self._agent:
            self._agent.refresh_task_sync(self)
        else:
            # In mock mode, simulate a status update
            if self.status == TaskStatus.PENDING:
                self.status = TaskStatus.RUNNING
            elif self.status == TaskStatus.RUNNING:
                self.status = TaskStatus.COMPLETED
                self.result = f"Simulated result for task {self.task_id}"
    
    def __str__(self) -> str:
        return f"CodegenTask(id={self.task_id}, status={self.status})"


class Agent:
    """
    Client for the Codegen Agent API.
    """
    
    def __init__(
        self, 
        org_id: str, 
        token: str, 
        api_endpoint: str = DEFAULT_API_ENDPOINT,
        mock_mode: bool = False
    ):
        """
        Initialize the Agent.
        
        Args:
            org_id: The organization ID
            token: The API token
            api_endpoint: The API endpoint URL
            mock_mode: Whether to run in mock mode (for testing)
        """
        self.org_id = org_id
        self.token = token
        self.api_endpoint = api_endpoint
        self.mock_mode = mock_mode
        logger.info(f"Initialized Agent for org_id: {org_id}")
    
    def run(self, prompt: str) -> CodegenTask:
        """
        Run the agent with the specified prompt.
        
        Args:
            prompt: The prompt to send to the agent
            
        Returns:
            A CodegenTask representing the running task
            
        Raises:
            CodegenApiError: If there's an error running the agent
        """
        logger.info(f"Running agent with prompt: {prompt[:100]}...")
        
        if self.mock_mode:
            # Create and return a mock task
            task_id = f"mock_task_{uuid.uuid4()}"
            return CodegenTask(task_id=task_id, agent=self)
        
        try:
            # Create a task via the API
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "organization_id": self.org_id,
                "prompt": prompt
            }
            
            with httpx.Client() as client:
                response = client.post(
                    f"{self.api_endpoint}/agents/run",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
            
            if response.status_code != 200:
                error_msg = f"Error creating task: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise CodegenApiError(
                    message=error_msg,
                    status_code=response.status_code,
                    response=response.json() if response.text else None
                )
            
            response_data = response.json()
            task_id = response_data.get("task_id")
            
            if not task_id:
                error_msg = "No task_id in response"
                logger.error(error_msg)
                raise CodegenApiError(message=error_msg, response=response_data)
            
            # Create and return a task
            return CodegenTask(task_id=task_id, agent=self)
            
        except httpx.RequestError as e:
            error_msg = f"Error connecting to Codegen API: {str(e)}"
            logger.error(error_msg)
            raise CodegenApiError(message=error_msg)
        
        except Exception as e:
            error_msg = f"Unexpected error running agent: {str(e)}"
            logger.error(error_msg)
            raise CodegenApiError(message=error_msg)
    
    async def run_async(self, prompt: str) -> CodegenTask:
        """
        Run the agent with the specified prompt asynchronously.
        
        Args:
            prompt: The prompt to send to the agent
            
        Returns:
            A CodegenTask representing the running task
            
        Raises:
            CodegenApiError: If there's an error running the agent
        """
        logger.info(f"Running agent asynchronously with prompt: {prompt[:100]}...")
        
        if self.mock_mode:
            # Create and return a mock task
            task_id = f"mock_task_{uuid.uuid4()}"
            return CodegenTask(task_id=task_id, agent=self)
        
        try:
            # Create a task via the API
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "organization_id": self.org_id,
                "prompt": prompt
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_endpoint}/agents/run",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
            
            if response.status_code != 200:
                error_msg = f"Error creating task: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise CodegenApiError(
                    message=error_msg,
                    status_code=response.status_code,
                    response=response.json() if response.text else None
                )
            
            response_data = response.json()
            task_id = response_data.get("task_id")
            
            if not task_id:
                error_msg = "No task_id in response"
                logger.error(error_msg)
                raise CodegenApiError(message=error_msg, response=response_data)
            
            # Create and return a task
            return CodegenTask(task_id=task_id, agent=self)
            
        except httpx.RequestError as e:
            error_msg = f"Error connecting to Codegen API: {str(e)}"
            logger.error(error_msg)
            raise CodegenApiError(message=error_msg)
        
        except Exception as e:
            error_msg = f"Unexpected error running agent: {str(e)}"
            logger.error(error_msg)
            raise CodegenApiError(message=error_msg)
    
    def refresh_task_sync(self, task: CodegenTask) -> None:
        """
        Refresh the task status synchronously.
        
        Args:
            task: The task to refresh
            
        Raises:
            CodegenApiError: If there's an error refreshing the task
        """
        if self.mock_mode:
            # Simulate a status update
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.RUNNING
            elif task.status == TaskStatus.RUNNING:
                task.status = TaskStatus.COMPLETED
                task.result = f"Simulated result for task {task.task_id}"
            return
        
        try:
            # Get task status via the API
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            with httpx.Client() as client:
                response = client.get(
                    f"{self.api_endpoint}/agents/tasks/{task.task_id}",
                    headers=headers,
                    timeout=30.0
                )
            
            if response.status_code != 200:
                error_msg = f"Error refreshing task: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise CodegenApiError(
                    message=error_msg,
                    status_code=response.status_code,
                    response=response.json() if response.text else None
                )
            
            response_data = response.json()
            
            # Update task with the latest status
            task.status = response_data.get("status", task.status)
            
            if task.status == TaskStatus.COMPLETED:
                task.result = response_data.get("result")
            elif task.status in [TaskStatus.FAILED, TaskStatus.ERROR]:
                task.error = response_data.get("error", "Unknown error")
            
        except httpx.RequestError as e:
            error_msg = f"Error connecting to Codegen API: {str(e)}"
            logger.error(error_msg)
            raise CodegenApiError(message=error_msg)
        
        except Exception as e:
            error_msg = f"Unexpected error refreshing task: {str(e)}"
            logger.error(error_msg)
            raise CodegenApiError(message=error_msg)
    
    async def refresh_task(self, task: CodegenTask) -> None:
        """
        Refresh the task status asynchronously.
        
        Args:
            task: The task to refresh
            
        Raises:
            CodegenApiError: If there's an error refreshing the task
        """
        if self.mock_mode:
            # Simulate a status update
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.RUNNING
            elif task.status == TaskStatus.RUNNING:
                task.status = TaskStatus.COMPLETED
                task.result = f"Simulated result for task {task.task_id}"
            return
        
        try:
            # Get task status via the API
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_endpoint}/agents/tasks/{task.task_id}",
                    headers=headers,
                    timeout=30.0
                )
            
            if response.status_code != 200:
                error_msg = f"Error refreshing task: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise CodegenApiError(
                    message=error_msg,
                    status_code=response.status_code,
                    response=response.json() if response.text else None
                )
            
            response_data = response.json()
            
            # Update task with the latest status
            task.status = response_data.get("status", task.status)
            
            if task.status == TaskStatus.COMPLETED:
                task.result = response_data.get("result")
            elif task.status in [TaskStatus.FAILED, TaskStatus.ERROR]:
                task.error = response_data.get("error", "Unknown error")
            
        except httpx.RequestError as e:
            error_msg = f"Error connecting to Codegen API: {str(e)}"
            logger.error(error_msg)
            raise CodegenApiError(message=error_msg)
        
        except Exception as e:
            error_msg = f"Unexpected error refreshing task: {str(e)}"
            logger.error(error_msg)
            raise CodegenApiError(message=error_msg)


class CodegenAgent:
    """
    A high-level wrapper around the Codegen Agent API.
    """
    
    def __init__(
        self, 
        org_id: str, 
        token: str, 
        api_endpoint: str = DEFAULT_API_ENDPOINT,
        mock_mode: bool = False
    ):
        """
        Initialize the Codegen Agent.
        
        Args:
            org_id: The organization ID
            token: The API token
            api_endpoint: The API endpoint URL
            mock_mode: Whether to run in mock mode (for testing)
        """
        self.org_id = org_id
        self.token = token
        self.api_endpoint = api_endpoint
        self.mock_mode = mock_mode
        logger.info(f"Initialized Codegen Agent for org_id: {org_id}")
    
    async def run(self, prompt: str) -> Dict[str, Any]:
        """
        Run the Codegen Agent with the specified prompt.
        
        Args:
            prompt: The prompt to send to the agent
            
        Returns:
            The result of the agent execution
        """
        logger.info(f"Running Codegen Agent with prompt: {prompt[:100]}...")
        
        try:
            # Create an agent
            agent = Agent(
                org_id=self.org_id, 
                token=self.token, 
                api_endpoint=self.api_endpoint,
                mock_mode=self.mock_mode
            )
            
            # Run the task
            task = agent.run(prompt)
            
            # Wait for completion
            while task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.ERROR]:
                await asyncio.sleep(1)
                await task.refresh()
            
            # Return the result
            if task.status == TaskStatus.COMPLETED:
                return {
                    "status": "completed",
                    "result": task.result
                }
            else:
                return {
                    "status": task.status,
                    "error": task.error or "Task did not complete successfully"
                }
            
        except CodegenApiError as e:
            logger.error(f"Error running Codegen Agent: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error running Codegen Agent: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

