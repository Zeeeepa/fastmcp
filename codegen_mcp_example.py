#!/usr/bin/env python3
"""
Example script demonstrating how to use the Codegen MCP server.
"""

import asyncio
import json
from fastmcp import Client

async def main():
    # Connect to the Codegen MCP server
    # This assumes the server is running using stdio transport
    async with Client("./codegen_mcp_server.py") as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool_name in tools:
            print(f"- {tool_name}")
        print()
        
        # Get server configuration
        config = await client.read_resource("codegen://config")
        print(f"Server configuration: {json.dumps(config.content, indent=2)}")
        print()
        
        # Get available templates
        templates = await client.read_resource("codegen://templates")
        print(f"Available templates: {', '.join(templates.content.keys())}")
        print()
        
        # Example: Create a PR
        print("Example: Creating a PR")
        try:
            # Replace with your actual credentials and query
            result = await client.call_tool("run_create_pr", {
                "query": "Create a PR that adds error handling to the login function",
                # Uncomment and add your credentials if not using environment variables
                # "org_id": "your-org-id",
                # "token": "your-api-token"
            })
            print(f"Result: {json.dumps(result.content, indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
        
        print()
        
        # Example: Create Linear issues
        print("Example: Creating Linear issues")
        try:
            # Replace with your actual credentials and query
            result = await client.call_tool("run_create_linear_issues", {
                "query": "Create a main issue for implementing user authentication with sub-issues for login, registration, password reset, and email verification",
                # Uncomment and add your credentials if not using environment variables
                # "org_id": "your-org-id",
                # "token": "your-api-token"
            })
            print(f"Result: {json.dumps(result.content, indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
        
        print()
        
        # Example: Using the generic tool
        print("Example: Using the generic tool")
        try:
            # Replace with your actual credentials and query
            result = await client.call_tool("run_codegen", {
                "template_id": "endpoint3",
                "query": "Analyze the performance of our API endpoints and suggest optimizations",
                # Uncomment and add your credentials if not using environment variables
                # "org_id": "your-org-id",
                # "token": "your-api-token"
            })
            print(f"Result: {json.dumps(result.content, indent=2)}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

