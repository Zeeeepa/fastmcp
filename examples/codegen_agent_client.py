"""
Codegen Agent MCP Client Example

This example demonstrates how to use the Codegen Agent MCP server from a client.
"""

import asyncio
import json
from fastmcp import Client

async def main():
    """
    Main function to demonstrate the client usage.
    """
    # Connect to the server
    print("Connecting to the Codegen Agent MCP server...")
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {json.dumps(tools, indent=2)}")
        
        # Get available prompt templates
        templates = await client.read_resource("prompts://templates")
        print(f"Available prompt templates: {json.dumps(list(templates.content.keys()), indent=2)}")
        
        # Example: Create a PR
        print("\n--- Example: Create a PR ---")
        result = await client.call_tool(
            "create_pr", 
            {
                "agent_query": "Create a PR that adds a new feature to calculate the factorial of a number"
            }
        )
        print(f"Result: {result.text}")
        
        # Example: Create Linear issues
        print("\n--- Example: Create Linear Issues ---")
        result = await client.call_tool(
            "create_linear_issues", 
            {
                "agent_query": "Create a main issue for implementing a new authentication system with sub-issues for login, registration, password reset, and user profile management"
            }
        )
        print(f"Result: {result.text}")
        
        # Example: Analyze codebase
        print("\n--- Example: Analyze Codebase ---")
        result = await client.call_tool(
            "analyze_codebase", 
            {
                "agent_query": "Analyze the codebase for performance bottlenecks and security vulnerabilities"
            }
        )
        print(f"Result: {result.text}")

if __name__ == "__main__":
    asyncio.run(main())

