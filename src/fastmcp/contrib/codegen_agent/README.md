# Codegen Agent API Integration

This module provides a wrapper around the Codegen Agent API for use with FastMCP.

## Features

- High-level and low-level API access
- Asynchronous and synchronous methods
- Proper error handling and status updates
- Support for customizable organization ID and API token
- Mock mode for testing without API access

## Installation

This module is included as part of the FastMCP package. No additional installation is required.

## Usage

### High-level API

The `CodegenAgent` class provides a high-level interface to the Codegen Agent API:

```python
import asyncio
from fastmcp.contrib.codegen_agent import CodegenAgent

async def main():
    # Create a Codegen Agent
    agent = CodegenAgent(
        org_id="your-org-id",
        token="your-api-token"
    )
    
    # Run the agent with a prompt
    result = await agent.run("Create a simple Python function to calculate the factorial of a number")
    
    # Print the result
    print(f"Status: {result['status']}")
    if result['status'] == "completed":
        print(f"Result: {result['result']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")

# Run the example
asyncio.run(main())
```

### Low-level API

The `Agent` class provides a lower-level interface with more control:

```python
import asyncio
from fastmcp.contrib.codegen_agent import Agent, TaskStatus

async def main():
    # Create an Agent
    agent = Agent(
        org_id="your-org-id",
        token="your-api-token"
    )
    
    # Run the agent with a prompt
    task = agent.run("Create a simple Python function to calculate the factorial of a number")
    
    # Poll for completion
    while task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.ERROR]:
        print(f"Task status: {task.status}")
        
        # Refresh the task status
        await task.refresh()
        
        # Wait before checking again
        await asyncio.sleep(1)
    
    # Check if the task completed successfully
    if task.status == TaskStatus.COMPLETED:
        print("Task completed successfully!")
        print(f"Result: {task.result}")
    else:
        print(f"Task failed with status: {task.status}")
        print(f"Error: {task.error or 'Unknown error'}")

# Run the example
asyncio.run(main())
```

### Mock Mode

For testing without API access, you can use mock mode:

```python
# Create a Codegen Agent in mock mode
agent = CodegenAgent(
    org_id="your-org-id",
    token="your-api-token",
    mock_mode=True
)
```

## API Reference

### `CodegenAgent`

A high-level wrapper around the Codegen Agent API.

#### Methods

- `__init__(org_id, token, api_endpoint=DEFAULT_API_ENDPOINT, mock_mode=False)`: Initialize the Codegen Agent.
- `run(prompt)`: Run the Codegen Agent with the specified prompt.

### `Agent`

Client for the Codegen Agent API.

#### Methods

- `__init__(org_id, token, api_endpoint=DEFAULT_API_ENDPOINT, mock_mode=False)`: Initialize the Agent.
- `run(prompt)`: Run the agent with the specified prompt (synchronous).
- `run_async(prompt)`: Run the agent with the specified prompt (asynchronous).
- `refresh_task_sync(task)`: Refresh the task status (synchronous).
- `refresh_task(task)`: Refresh the task status (asynchronous).

### `CodegenTask`

Represents a task executed by the Codegen Agent.

#### Methods

- `__init__(task_id, status=TaskStatus.PENDING, agent=None)`: Initialize a Codegen Task.
- `refresh()`: Refresh the task status (asynchronous).
- `refresh_sync()`: Refresh the task status (synchronous).

### `TaskStatus`

Enum representing the possible statuses of a Codegen Agent task.

- `PENDING`: The task is pending.
- `RUNNING`: The task is running.
- `COMPLETED`: The task has completed successfully.
- `FAILED`: The task has failed.
- `ERROR`: An error occurred while running the task.

### `CodegenApiError`

Exception raised for errors in the Codegen API.

## Environment Variables

- `CODEGEN_ORG_ID`: The default organization ID to use.
- `CODEGEN_TOKEN`: The default API token to use.

## Error Handling

The module provides comprehensive error handling:

```python
from fastmcp.contrib.codegen_agent import CodegenAgent, CodegenApiError

try:
    agent = CodegenAgent(org_id="your-org-id", token="your-api-token")
    result = await agent.run("Your prompt here")
except CodegenApiError as e:
    print(f"API Error: {e.message}")
    if e.status_code:
        print(f"Status Code: {e.status_code}")
    if e.response:
        print(f"Response: {e.response}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

