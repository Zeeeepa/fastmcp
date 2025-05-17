"""
Example of using the Codegen Agent MCP Client.

This script demonstrates how to create a client for the Codegen Agent MCP Server.
"""

import asyncio
from fastmcp.client import Client

async def main():
    # Create a client for the Codegen Agent MCP Server
    client = Client("http://127.0.0.1:8000")
    
    # Connect to the server
    await client.connect()
    
    # Print server information
    print(f"Connected to: {client.server_name}")
    print(f"Instructions: {client.instructions}")
    
    # Get available tools
    tools = await client.list_tools()
    print("\nAvailable tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    # Get available prompts
    prompts = await client.list_prompts()
    print("\nAvailable prompts:")
    for prompt in prompts:
        print(f"- {prompt.name}: {prompt.description}")
    
    # Get available resources
    resources = await client.list_resources()
    print("\nAvailable resources:")
    for resource in resources:
        print(f"- {resource.uri}: {resource.description}")
    
    # Example: Generate code
    print("\nGenerating code...")
    result = await client.call_tool(
        "generate_code",
        description="Create a function that calculates the factorial of a number",
        language="python"
    )
    print(f"Result: {result}")
    
    # Example: Get prompt templates
    print("\nGetting prompt templates...")
    templates = await client.get_resource("codegen://prompts")
    print(f"Templates: {templates}")
    
    # Example: Get specific prompt template
    print("\nGetting code generation prompt template...")
    template = await client.get_resource("codegen://prompts/code_generation")
    print(f"Template: {template}")
    
    # Close the client
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())

