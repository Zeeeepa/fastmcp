# Codegen Agent MCP Server

This example demonstrates how to create a FastMCP server that integrates with the Codegen Agent API. The server provides 6 callable endpoints that execute the Codegen Agent with different prompt templates.

## Features

- 6 callable endpoints for different Codegen Agent operations
- Customizable prompt templates
- Asynchronous execution with status updates
- Optional organization ID and API token parameters

## Endpoints

1. **create_pr** - Creates a PR with the specified changes
2. **create_linear_issues** - Creates a main issue and sub-issues in Linear
3. **analyze_codebase** - Analyzes a codebase and provides insights
4. **fix_bug** - Fixes a bug in the codebase
5. **review_pr** - Reviews a PR and provides feedback
6. **generate_documentation** - Generates documentation for a codebase

## Usage

### Running the Server

```bash
# Install dependencies
pip install fastmcp

# Set environment variables (optional)
export CODEGEN_ORG_ID="your-org-id"
export CODEGEN_TOKEN="your-api-token"

# Run the server
python codegen_agent_server.py
```

The server will start on `http://127.0.0.1:8000` by default.

### Client Example

Here's an example of how to use the server from a Python client:

```python
from fastmcp import Client

async def main():
    # Connect to the server
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Create a PR
        result = await client.call_tool(
            "create_pr", 
            {
                "agent_query": "Create a PR that adds a new feature to calculate the factorial of a number",
                "org_id": "your-org-id",  # Optional
                "token": "your-api-token"  # Optional
            }
        )
        print(f"Result: {result.text}")

# Run the client
import asyncio
asyncio.run(main())
```

## Prompt Templates

Each endpoint uses a specific prompt template that guides the Codegen Agent's behavior. You can view the available templates using the `prompts://templates` resource:

```python
templates = await client.read_resource("prompts://templates")
print(templates.content)
```

You can also view a specific template:

```python
template = await client.read_resource("prompts://templates/create_pr")
print(template.content)
```

## Customization

You can customize the prompt templates by modifying the `PROMPT_TEMPLATES` dictionary in the `codegen_agent_server.py` file.

## Environment Variables

- `CODEGEN_ORG_ID` - The default organization ID to use
- `CODEGEN_TOKEN` - The default API token to use

## Notes

This example includes a mock implementation of the Codegen Agent API for demonstration purposes. In a real implementation, you would use the actual Codegen Agent library:

```python
from codegen import Agent

# Create an agent
agent = Agent(org_id="your-org-id", token="your-api-token")

# Run on task
task = agent.run("Your prompt here")

# Refresh to get updated status
task.refresh()
print(task.status)

# Once task is complete, you can access the result
if task.status == "completed":
    print(task.result)
```

