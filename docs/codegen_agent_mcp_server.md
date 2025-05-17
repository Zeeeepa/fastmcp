# Codegen Agent MCP Server Documentation

## Overview

The Codegen Agent MCP Server is a FastMCP implementation that integrates with the Codegen Agent API. It provides 6 callable endpoints that execute the Codegen Agent with different prompt templates, allowing you to leverage the power of Codegen's AI capabilities through a standardized Model Context Protocol (MCP) interface.

## Table of Contents

- [Server Setup and Configuration](#server-setup-and-configuration)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [Endpoints and Parameters](#endpoints-and-parameters)
  - [create_pr](#create_pr)
  - [create_linear_issues](#create_linear_issues)
  - [analyze_codebase](#analyze_codebase)
  - [fix_bug](#fix_bug)
  - [review_pr](#review_pr)
  - [generate_documentation](#generate_documentation)
- [Prompt Templates](#prompt-templates)
  - [Viewing Templates](#viewing-templates)
  - [Customizing Templates](#customizing-templates)
- [Usage Examples](#usage-examples)
  - [Basic Client Example](#basic-client-example)
  - [Advanced Usage Examples](#advanced-usage-examples)
- [API Reference](#api-reference)
  - [Tools](#tools)
  - [Resources](#resources)
- [Deployment](#deployment)
  - [Local Deployment](#local-deployment)
  - [Docker Deployment](#docker-deployment)
  - [Cloud Deployment](#cloud-deployment)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Debugging](#debugging)

## Server Setup and Configuration

### Prerequisites

Before setting up the Codegen Agent MCP Server, ensure you have the following:

- Python 3.8 or higher
- A Codegen account with API access
- Your Codegen organization ID and API token

### Installation

1. Install the required packages:

```bash
pip install fastmcp
```

2. If you plan to use the actual Codegen Agent API (not the mock implementation), install the Codegen SDK:

```bash
pip install codegen
```

### Environment Variables

The server uses the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `CODEGEN_ORG_ID` | Your Codegen organization ID | "323" (example) |
| `CODEGEN_TOKEN` | Your Codegen API token | "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99" (example) |

You can set these variables in your environment:

```bash
export CODEGEN_ORG_ID="your-org-id"
export CODEGEN_TOKEN="your-api-token"
```

Or provide them directly when calling the endpoints.

### Running the Server

To run the server:

1. Copy the `examples/codegen_agent_server.py` and `examples/codegen_agent.py` files to your project directory.
2. Run the server:

```bash
python codegen_agent_server.py
```

The server will start on `http://127.0.0.1:8000` by default. You can access the MCP endpoint at `http://127.0.0.1:8000/mcp`.

## Endpoints and Parameters

The server provides 6 callable endpoints, each executing the Codegen Agent with a different prompt template.

### create_pr

Creates a pull request with the specified changes.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_query` | string | Yes | The query describing what changes to make and PR details |
| `org_id` | string | No | The organization ID (defaults to `CODEGEN_ORG_ID` environment variable) |
| `token` | string | No | The API token (defaults to `CODEGEN_TOKEN` environment variable) |

**Example:**

```python
result = await client.call_tool(
    "create_pr", 
    {
        "agent_query": "Create a PR that adds a new feature to calculate the factorial of a number"
    }
)
```

### create_linear_issues

Creates a main issue and sub-issues in Linear.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_query` | string | Yes | The query describing the issues to create |
| `org_id` | string | No | The organization ID (defaults to `CODEGEN_ORG_ID` environment variable) |
| `token` | string | No | The API token (defaults to `CODEGEN_TOKEN` environment variable) |

**Example:**

```python
result = await client.call_tool(
    "create_linear_issues", 
    {
        "agent_query": "Create a main issue for implementing a new authentication system with sub-issues for login, registration, password reset, and user profile management"
    }
)
```

### analyze_codebase

Analyzes a codebase and provides insights.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_query` | string | Yes | The query describing what to analyze |
| `org_id` | string | No | The organization ID (defaults to `CODEGEN_ORG_ID` environment variable) |
| `token` | string | No | The API token (defaults to `CODEGEN_TOKEN` environment variable) |

**Example:**

```python
result = await client.call_tool(
    "analyze_codebase", 
    {
        "agent_query": "Analyze the codebase for performance bottlenecks and security vulnerabilities"
    }
)
```

### fix_bug

Fixes a bug in the codebase.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_query` | string | Yes | The query describing the bug to fix |
| `org_id` | string | No | The organization ID (defaults to `CODEGEN_ORG_ID` environment variable) |
| `token` | string | No | The API token (defaults to `CODEGEN_TOKEN` environment variable) |

**Example:**

```python
result = await client.call_tool(
    "fix_bug", 
    {
        "agent_query": "Fix the login form validation bug that allows empty passwords"
    }
)
```

### review_pr

Reviews a PR and provides feedback.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_query` | string | Yes | The query describing the PR to review |
| `org_id` | string | No | The organization ID (defaults to `CODEGEN_ORG_ID` environment variable) |
| `token` | string | No | The API token (defaults to `CODEGEN_TOKEN` environment variable) |

**Example:**

```python
result = await client.call_tool(
    "review_pr", 
    {
        "agent_query": "Review PR #123 for code quality and potential bugs"
    }
)
```

### generate_documentation

Generates documentation for a codebase.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_query` | string | Yes | The query describing what documentation to generate |
| `org_id` | string | No | The organization ID (defaults to `CODEGEN_ORG_ID` environment variable) |
| `token` | string | No | The API token (defaults to `CODEGEN_TOKEN` environment variable) |

**Example:**

```python
result = await client.call_tool(
    "generate_documentation", 
    {
        "agent_query": "Generate API documentation for the user authentication module"
    }
)
```

## Prompt Templates

Each endpoint uses a specific prompt template that guides the Codegen Agent's behavior. These templates are defined in the `PROMPT_TEMPLATES` dictionary in the `codegen_agent_server.py` file.

### Viewing Templates

You can view the available templates using the `prompts://templates` resource:

```python
templates = await client.read_resource("prompts://templates")
print(templates.content)
```

You can also view a specific template:

```python
template = await client.read_resource("prompts://templates/create_pr")
print(template.content)
```

### Customizing Templates

You can customize the prompt templates by modifying the `PROMPT_TEMPLATES` dictionary in the `codegen_agent_server.py` file:

```python
PROMPT_TEMPLATES = {
    "create_pr": """
    Create a PR with the following specifications:
    
    {agent_query}
    
    Instructions:
    - Create a new branch from the main branch
    - Make the necessary changes
    - Create a PR with a descriptive title and body
    - Link any relevant issues
    """,
    
    # Other templates...
}
```

Each template can include the `{agent_query}` placeholder, which will be replaced with the query provided when calling the endpoint.

## Usage Examples

### Basic Client Example

Here's a basic example of how to use the server from a Python client:

```python
import asyncio
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
                "agent_query": "Create a PR that adds a new feature to calculate the factorial of a number"
            }
        )
        print(f"Result: {result.text}")

# Run the client
asyncio.run(main())
```

### Advanced Usage Examples

#### Listing Available Tools and Templates

```python
import asyncio
import json
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {json.dumps(tools, indent=2)}")
        
        # Get available prompt templates
        templates = await client.read_resource("prompts://templates")
        print(f"Available prompt templates: {json.dumps(list(templates.content.keys()), indent=2)}")

asyncio.run(main())
```

#### Using Custom Organization ID and Token

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool(
            "create_pr", 
            {
                "agent_query": "Create a PR that adds a new feature to calculate the factorial of a number",
                "org_id": "your-custom-org-id",
                "token": "your-custom-token"
            }
        )
        print(f"Result: {result.text}")

asyncio.run(main())
```

#### Creating Linear Issues

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool(
            "create_linear_issues", 
            {
                "agent_query": "Create a main issue for implementing a new authentication system with sub-issues for login, registration, password reset, and user profile management"
            }
        )
        print(f"Result: {result.text}")

asyncio.run(main())
```

## API Reference

### Tools

The server provides the following tools:

| Tool | Description |
|------|-------------|
| `create_pr` | Creates a PR with the specified changes |
| `create_linear_issues` | Creates a main issue and sub-issues in Linear |
| `analyze_codebase` | Analyzes a codebase and provides insights |
| `fix_bug` | Fixes a bug in the codebase |
| `review_pr` | Reviews a PR and provides feedback |
| `generate_documentation` | Generates documentation for a codebase |

### Resources

The server provides the following resources:

| Resource | Description |
|----------|-------------|
| `prompts://templates` | Returns all available prompt templates |
| `prompts://templates/{template_name}` | Returns a specific prompt template |

## Deployment

### Local Deployment

To deploy the server locally:

1. Install the required packages:

```bash
pip install fastmcp
```

2. Set the environment variables:

```bash
export CODEGEN_ORG_ID="your-org-id"
export CODEGEN_TOKEN="your-api-token"
```

3. Run the server:

```bash
python codegen_agent_server.py
```

### Docker Deployment

To deploy the server using Docker:

1. Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY codegen_agent_server.py .
COPY codegen_agent.py .

ENV CODEGEN_ORG_ID="your-org-id"
ENV CODEGEN_TOKEN="your-api-token"

EXPOSE 8000

CMD ["python", "codegen_agent_server.py"]
```

2. Create a requirements.txt file:

```
fastmcp
```

3. Build and run the Docker image:

```bash
docker build -t codegen-agent-mcp-server .
docker run -p 8000:8000 codegen-agent-mcp-server
```

### Cloud Deployment

To deploy the server on a cloud platform like AWS, Azure, or Google Cloud:

1. Package your application as a Docker container (see Docker Deployment).
2. Deploy the container to your cloud provider's container service (e.g., AWS ECS, Azure Container Instances, Google Cloud Run).
3. Set the environment variables in your cloud provider's configuration.
4. Ensure the server is accessible via HTTP/HTTPS.

## Troubleshooting

### Common Issues

#### Connection Refused

If you get a "Connection refused" error when trying to connect to the server, ensure:

- The server is running
- You're using the correct host and port
- There are no firewall rules blocking the connection

#### Authentication Errors

If you get authentication errors when using the Codegen Agent API:

- Check that your organization ID and API token are correct
- Ensure your API token has the necessary permissions
- Verify that your Codegen account is active

### Debugging

To enable more verbose logging, modify the logging configuration in the `codegen_agent.py` file:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

You can also add more detailed logging in the `run_codegen_agent` function in `codegen_agent_server.py`:

```python
async def run_codegen_agent(
    prompt_template: str, 
    agent_query: str, 
    ctx: Context,
    org_id: str = DEFAULT_ORG_ID,
    token: str = DEFAULT_TOKEN
) -> Dict[str, Any]:
    # Add more detailed logging
    await ctx.info(f"Starting Codegen Agent execution with template: {prompt_template}")
    await ctx.info(f"Using organization ID: {org_id}")
    await ctx.info(f"Agent query: {agent_query}")
    
    # Rest of the function...
```

