# Codegen Agent MCP Server Quick Start Guide

This guide will help you quickly set up and start using the Codegen Agent MCP Server.

## Prerequisites

- Python 3.8 or higher
- A Codegen account with API access
- Your Codegen organization ID and API token

## Installation

1. Install the required packages:

```bash
pip install fastmcp
```

2. Clone the repository or copy the example files:

```bash
# If cloning the repository
git clone https://github.com/Zeeeepa/fastmcp.git
cd fastmcp

# Or copy the example files directly
mkdir codegen_agent_mcp
cd codegen_agent_mcp
curl -O https://raw.githubusercontent.com/Zeeeepa/fastmcp/main/examples/codegen_agent_server.py
curl -O https://raw.githubusercontent.com/Zeeeepa/fastmcp/main/examples/codegen_agent.py
```

## Configuration

Set your Codegen organization ID and API token as environment variables:

```bash
export CODEGEN_ORG_ID="your-org-id"
export CODEGEN_TOKEN="your-api-token"
```

## Running the Server

Start the server:

```bash
python codegen_agent_server.py
```

The server will start on `http://127.0.0.1:8000` by default.

## Using the Server

Here's a simple client example to test the server:

```python
import asyncio
from fastmcp import Client

async def main():
    # Connect to the server
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Call an endpoint
        result = await client.call_tool(
            "create_pr", 
            {
                "agent_query": "Create a PR that adds a new feature to calculate the factorial of a number"
            }
        )
        print(f"Result: {result.text}")

# Run the client
asyncio.run(main())
```

Save this as `test_client.py` and run it:

```bash
python test_client.py
```

## Available Endpoints

The server provides 6 callable endpoints:

1. `create_pr` - Creates a PR with the specified changes
2. `create_linear_issues` - Creates a main issue and sub-issues in Linear
3. `analyze_codebase` - Analyzes a codebase and provides insights
4. `fix_bug` - Fixes a bug in the codebase
5. `review_pr` - Reviews a PR and provides feedback
6. `generate_documentation` - Generates documentation for a codebase

## Next Steps

For more detailed information, see the [full documentation](codegen_agent_mcp_server.md).

