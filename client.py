import requests
import json
import time
from typing import Dict, Any, Optional

class MCPClient:
    """Client for interacting with the MCP Prompt Template Server"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the MCP client
        
        Args:
            base_url: The base URL of the MCP server
        """
        self.base_url = base_url.rstrip('/')
    
    def execute_pr_creation(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute PR creation template with the given context
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            Task information including ID and status
        """
        return self._execute_endpoint("pr-creation", context, additional_params)
    
    def execute_linear_issues(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute Linear issues template with the given context
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            Task information including ID and status
        """
        return self._execute_endpoint("linear-issues", context, additional_params)
    
    def execute_code_generation(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute code generation template with the given context
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            Task information including ID and status
        """
        return self._execute_endpoint("code-generation", context, additional_params)
    
    def execute_data_analysis(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute data analysis template with the given context
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            Task information including ID and status
        """
        return self._execute_endpoint("data-analysis", context, additional_params)
    
    def execute_documentation(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute documentation template with the given context
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            Task information including ID and status
        """
        return self._execute_endpoint("documentation", context, additional_params)
    
    def execute_testing_strategy(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute testing strategy template with the given context
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            Task information including ID and status
        """
        return self._execute_endpoint("testing-strategy", context, additional_params)
    
    def _execute_endpoint(self, endpoint: str, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a specific endpoint with the given context
        
        Args:
            endpoint: The endpoint name
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            Task information including ID and status
        """
        if additional_params is None:
            additional_params = {}
            
        url = f"{self.base_url}/api/{endpoint}"
        payload = {
            "context": context,
            "additional_params": additional_params
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a task
        
        Args:
            task_id: The ID of the task
            
        Returns:
            Task information including status and result if available
        """
        url = f"{self.base_url}/api/tasks/{task_id}"
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def list_tasks(self) -> Dict[str, Any]:
        """List all tasks
        
        Returns:
            List of all tasks
        """
        url = f"{self.base_url}/api/tasks"
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def wait_for_task_completion(self, task_id: str, timeout: int = 600, polling_interval: int = 5) -> Dict[str, Any]:
        """Wait for a task to complete
        
        Args:
            task_id: The ID of the task
            timeout: Maximum time to wait in seconds
            polling_interval: Time between status checks in seconds
            
        Returns:
            The completed task information
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            task_info = self.get_task_status(task_id)
            
            if task_info["status"] in ["completed", "failed"]:
                return task_info
            
            time.sleep(polling_interval)
        
        raise TimeoutError(f"Task {task_id} did not complete within the specified timeout of {timeout} seconds")

# Usage example
if __name__ == "__main__":
    client = MCPClient()
    
    # Example: Create a PR
    response = client.execute_pr_creation(
        context="Create a pull request for adding user authentication features. The changes include new login/logout endpoints, JWT token handling, and user session management."
    )
    
    print(f"Task created with ID: {response['task_id']}")
    
    # Wait for the task to complete
    result = client.wait_for_task_completion(response['task_id'])
    
    print(f"Task status: {result['status']}")
    if result['status'] == 'completed':
        print(f"Result: {json.dumps(result['result'], indent=2)}")
