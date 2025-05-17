# MCP Prompt Template Server

A modular MCP server with 6 specialized prompt template endpoints for agent-based code generation, PR creation, Linear issue management, and more.

## Overview

This server provides a standardized interface for leveraging the Codegen Agent API with specialized prompt templates for different use cases. It exposes 6 endpoints that format inputs according to specialized templates before executing them through the Codegen Agent.

## Available Endpoints

1. **PR Creation**: Generate GitHub PR descriptions and metadata
2. **Linear Issues**: Create structured main issues and sub-issues for Linear
3. **Code Generation**: Generate optimized code implementations
4. **Data Analysis**: Analyze data and provide insights
5. **Documentation**: Create comprehensive documentation
6. **Testing Strategy**: Develop testing approaches and test cases

## Installation

```bash
# Clone the repository
git clone https://github.com/Zeeeepa/fastmcp.git
cd fastmcp

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
python mcp_server.py
```

The server will start on port 8000 by default.

### Using the Client

```python
from client import MCPClient

# Initialize the client
client = MCPClient()

# Execute PR creation
response = client.execute_pr_creation(
    context="Create a pull request for adding user authentication features."
)

# Get task ID
task_id = response['task_id']

# Wait for task completion
result = client.wait_for_task_completion(task_id)

# Print the result
print(result['result'])
```

## Environment Variables

The following environment variables can be set:

- `ORG_ID`: Your organization ID (default: "323")
- `API_TOKEN`: Your API token (default: "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

## API Reference

### POST /api/pr-creation

Generate PR descriptions and metadata.

### POST /api/linear-issues

Create structured main and sub-issues for Linear.

### POST /api/code-generation

Generate optimized code implementations.

### POST /api/data-analysis

Analyze data and provide insights.

### POST /api/documentation

Create comprehensive documentation.

### POST /api/testing-strategy

Develop testing approaches and test cases.

### GET /api/tasks/{task_id}

Get the status and result of a specific task.

### GET /api/tasks

List all tasks.

## License

MIT
