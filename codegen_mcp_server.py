#!/usr/bin/env python3
"""
Codegen MCP Server - A FastMCP server that provides tools to execute Codegen Agent tasks.

This server exposes 6 callable endpoints that execute Codegen Agent tasks with
different templates:
1. Create PR
2. Create a main issue and sub-issues on Linear
3-6. Additional customizable endpoints

Each endpoint uses the same underlying function with different prompt templates.
"""

import os
import asyncio
from typing import Dict, Any, Optional
from fastmcp import FastMCP, Context

# Import the Codegen SDK
try:
    from codegen import Agent
except ImportError:
    print("Codegen SDK not found. Please install it with: pip install codegen")
    print("For now, we'll use a mock implementation for demonstration purposes.")

    class MockTask:
        def __init__(self, prompt):
            self.prompt = prompt
            self.status = "pending"
            self.result = None
        
        def refresh(self):
            # Simulate task completion
            self.status = "completed"
            self.result = f"Completed task with prompt: {self.prompt}"
    
    class Agent:
        def __init__(self, org_id=None, token=None):
            self.org_id = org_id
            self.token = token
        
        def run(self, prompt):
            return MockTask(prompt)

# Create the MCP server
mcp = FastMCP("Codegen MCP Server")

# Define the templates for each endpoint
TEMPLATES = {
    "create_pr": {
        "name": "Create PR",
        "description": "Creates a pull request using Codegen Agent",
        "template": "{PromptTemplate1(withPRsettinginstructions(ihavethispromptmyself)+agentinputquery}"
    },
    "create_linear_issues": {
        "name": "Create Linear Issues",
        "description": "Creates a main issue and sub-issues on Linear using Codegen Agent",
        "template": "{PromptTemplate2(withLinearsettinginstructions(ihavethispromptmyself)+agentinputquery}"
    },
    "endpoint3": {
        "name": "Custom Endpoint 3",
        "description": "Custom endpoint 3 using Codegen Agent",
        "template": "{PromptTemplate3+agentinputquery}"
    },
    "endpoint4": {
        "name": "Custom Endpoint 4",
        "description": "Custom endpoint 4 using Codegen Agent",
        "template": "{PromptTemplate4+agentinputquery}"
    },
    "endpoint5": {
        "name": "Custom Endpoint 5",
        "description": "Custom endpoint 5 using Codegen Agent",
        "template": "{PromptTemplate5+agentinputquery}"
    },
    "endpoint6": {
        "name": "Custom Endpoint 6",
        "description": "Custom endpoint 6 using Codegen Agent",
        "template": "{PromptTemplate6+agentinputquery}"
    }
}

# Configuration resource
@mcp.resource("codegen://config")
def get_config():
    """Get the Codegen MCP Server configuration."""
    return {
        "version": "1.0.0",
        "endpoints": list(TEMPLATES.keys()),
        "description": "Codegen MCP Server provides tools to execute Codegen Agent tasks."
    }

# Templates resource
@mcp.resource("codegen://templates")
def get_templates():
    """Get all available templates."""
    return TEMPLATES

# Template resource
@mcp.resource("codegen://templates/{template_id}")
def get_template(template_id: str):
    """Get a specific template by ID."""
    if template_id not in TEMPLATES:
        raise ValueError(f"Template '{template_id}' not found")
    return TEMPLATES[template_id]

# Core function to run a Codegen Agent task
async def run_codegen_task(
    template_id: str, 
    query: str, 
    org_id: Optional[str] = None, 
    token: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Run a Codegen Agent task with the specified template and query.
    
    Args:
        template_id: The ID of the template to use
        query: The query to send to the agent
        org_id: Optional organization ID (defaults to environment variable)
        token: Optional API token (defaults to environment variable)
        ctx: Optional MCP context for progress reporting
    
    Returns:
        A dictionary with the task result
    """
    if template_id not in TEMPLATES:
        raise ValueError(f"Template '{template_id}' not found")
    
    # Get credentials from parameters or environment variables
    org_id = org_id or os.environ.get("CODEGEN_ORG_ID")
    token = token or os.environ.get("CODEGEN_API_TOKEN")
    
    if not org_id or not token:
        raise ValueError("Missing Codegen credentials. Provide org_id and token parameters or set CODEGEN_ORG_ID and CODEGEN_API_TOKEN environment variables.")
    
    # Create the agent
    agent = Agent(org_id=org_id, token=token)
    
    # Construct the prompt using the template
    template = TEMPLATES[template_id]["template"]
    prompt = template.replace("agentinputquery", query)
    
    if ctx:
        await ctx.info(f"Starting Codegen task with template: {template_id}")
        await ctx.info(f"Query: {query}")
    
    # Run the task
    task = agent.run(prompt)
    
    # Poll for completion
    if ctx:
        await ctx.info("Task submitted, waiting for completion...")
    
    # Simple polling mechanism
    while True:
        task.refresh()
        if task.status == "completed":
            if ctx:
                await ctx.info("Task completed successfully!")
            break
        elif task.status == "failed":
            error_msg = "Task failed"
            if ctx:
                await ctx.error(error_msg)
            raise RuntimeError(error_msg)
        
        if ctx:
            await ctx.report_progress(0.5, "Task in progress...")
        
        # Wait before checking again
        await asyncio.sleep(2)
    
    # Return the result
    return {
        "status": task.status,
        "result": task.result,
        "template_id": template_id,
        "query": query
    }

# Create tools for each template
for template_id, template_info in TEMPLATES.items():
    # Use a factory function to capture the template_id in the closure
    def create_tool(tid):
        @mcp.tool(name=f"run_{tid}")
        async def tool_fn(
            query: str,
            org_id: Optional[str] = None,
            token: Optional[str] = None,
            ctx: Context = None
        ) -> Dict[str, Any]:
            """
            Run a Codegen Agent task with the specified template and query.
            
            Args:
                query: The query to send to the agent
                org_id: Optional organization ID (defaults to environment variable)
                token: Optional API token (defaults to environment variable)
            
            Returns:
                A dictionary with the task result
            """
            return await run_codegen_task(tid, query, org_id, token, ctx)
        
        # Update the tool's docstring with the template description
        tool_fn.__doc__ = f"{template_info['description']}\n\n{tool_fn.__doc__}"
        
        return tool_fn
    
    # Create the tool
    create_tool(template_id)

# Generic tool that can use any template
@mcp.tool()
async def run_codegen(
    template_id: str,
    query: str,
    org_id: Optional[str] = None,
    token: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Run a Codegen Agent task with the specified template and query.
    
    Args:
        template_id: The ID of the template to use
        query: The query to send to the agent
        org_id: Optional organization ID (defaults to environment variable)
        token: Optional API token (defaults to environment variable)
    
    Returns:
        A dictionary with the task result
    """
    return await run_codegen_task(template_id, query, org_id, token, ctx)

# Run the server if executed directly
if __name__ == "__main__":
    # Determine the transport from environment variable or default to stdio
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    
    if transport == "streamable-http":
        host = os.environ.get("MCP_HOST", "127.0.0.1")
        port = int(os.environ.get("MCP_PORT", "8000"))
        path = os.environ.get("MCP_PATH", "/mcp")
        mcp.run(transport=transport, host=host, port=port, path=path)
    elif transport == "sse":
        host = os.environ.get("MCP_HOST", "127.0.0.1")
        port = int(os.environ.get("MCP_PORT", "8000"))
        mcp.run(transport=transport, host=host, port=port)
    else:
        # Default to stdio
        mcp.run(transport="stdio")
