# Codegen MCP Server

A FastMCP server that provides tools to execute Codegen Agent tasks through the Model Context Protocol (MCP).

## Overview

This MCP server exposes 6 callable endpoints that execute Codegen Agent tasks with different templates:

1. **Create PR** - Creates a pull request using Codegen Agent
2. **Create Linear Issues** - Creates a main issue and sub-issues on Linear using Codegen Agent
3. **Custom Endpoint 3** - Customizable endpoint for additional functionality
4. **Custom Endpoint 4** - Customizable endpoint for additional functionality
5. **Custom Endpoint 5** - Customizable endpoint for additional functionality
6. **Custom Endpoint 6** - Customizable endpoint for additional functionality

Each endpoint uses the same underlying function with different prompt templates, allowing you to standardize the execution pattern while customizing the prompts for specific tasks.

## Installation

1. Install the required dependencies:

```bash
pip install fastmcp codegen
```

2. Set up your Codegen credentials as environment variables:

```bash
export CODEGEN_ORG_ID="your-org-id"
export CODEGEN_API_TOKEN="your-api-token"
```

## Usage

### Running the Server

You can run the server using different transport protocols:

#### STDIO (Default)

```bash
python codegen_mcp_server.py
```

#### Streamable HTTP

```bash
export MCP_TRANSPORT="streamable-http"
export MCP_HOST="127.0.0.1"
export MCP_PORT="8000"
export MCP_PATH="/mcp"
python codegen_mcp_server.py
```

#### Server-Sent Events (SSE)

```bash
export MCP_TRANSPORT="sse"
export MCP_HOST="127.0.0.1"
export MCP_PORT="8000"
python codegen_mcp_server.py
```

### Connecting to the Server

You can connect to the server using any MCP client. Here's an example using FastMCP's client:

```python
from fastmcp import Client

async def main():
    # Connect to the server
    async with Client("path/to/codegen_mcp_server.py") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Call a specific tool
        result = await client.call_tool("run_create_pr", {
            "query": "Create a PR that adds error handling to the login function",
            "org_id": "your-org-id",  # Optional, can use environment variable
            "token": "your-api-token"  # Optional, can use environment variable
        })
        print(f"Result: {result.content}")

# Run the async function
import asyncio
asyncio.run(main())
```

## Available Tools

### Specific Template Tools

Each template has its own dedicated tool:

- `run_create_pr` - Creates a pull request
- `run_create_linear_issues` - Creates a main issue and sub-issues on Linear
- `run_endpoint3` - Custom endpoint 3
- `run_endpoint4` - Custom endpoint 4
- `run_endpoint5` - Custom endpoint 5
- `run_endpoint6` - Custom endpoint 6

### Generic Tool

There's also a generic tool that can use any template:

- `run_codegen` - Runs a Codegen Agent task with a specified template

Example:
```python
result = await client.call_tool("run_codegen", {
    "template_id": "create_pr",
    "query": "Create a PR that adds error handling to the login function",
    "org_id": "your-org-id",  # Optional
    "token": "your-api-token"  # Optional
})
```

## Resources

The server also provides resources for discovering available templates:

- `codegen://config` - Server configuration information
- `codegen://templates` - List of all available templates
- `codegen://templates/{template_id}` - Details for a specific template

Example:
```python
config = await client.read_resource("codegen://config")
templates = await client.read_resource("codegen://templates")
create_pr_template = await client.read_resource("codegen://templates/create_pr")
```

## Customizing Templates

You can customize the templates by modifying the `TEMPLATES` dictionary in the `codegen_mcp_server.py` file:

```python
TEMPLATES = {
    "create_pr": {
        "name": "Create PR",
        "description": "Creates a pull request using Codegen Agent",
        "template": "{PromptTemplate1(withPRsettinginstructions(ihavethispromptmyself)+agentinputquery}"
    },
    # Add or modify other templates...
}
```

## Advanced Usage

### Integration with LLM Applications

This MCP server can be integrated with any LLM application that supports the Model Context Protocol, such as:

- Claude Desktop
- Cursor
- Lovable
- Windsurf
- Other MCP-compatible applications

### Using with Claude Desktop

1. Install the server in Claude Desktop:

```bash
fastmcp claude install codegen_mcp_server.py:mcp
```

2. Open Claude Desktop and use the tools directly in your conversations.

## Troubleshooting

- **Missing Credentials**: Ensure you've set the `CODEGEN_ORG_ID` and `CODEGEN_API_TOKEN` environment variables or provide them as parameters when calling the tools.
- **Connection Issues**: Verify that the server is running and that you're using the correct transport protocol and connection details.
- **Task Failures**: Check the error messages returned by the Codegen Agent for more information about why a task failed.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

