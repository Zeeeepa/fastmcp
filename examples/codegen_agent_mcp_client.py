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
        
        # Example: Generate code
        print("\n--- Example: Generate Code ---")
        result = await client.call_tool(
            "generate_code", 
            {
                "description": "Create a function to calculate the factorial of a number",
                "language": "python",
                "mock_mode": True
            }
        )
        print(f"Result: {result.text}")
        
        # Example: Explain code
        print("\n--- Example: Explain Code ---")
        result = await client.call_tool(
            "explain_code", 
            {
                "code": """
                def factorial(n):
                    if n == 0 or n == 1:
                        return 1
                    else:
                        return n * factorial(n-1)
                """,
                "mock_mode": True
            }
        )
        print(f"Result: {result.text}")
        
        # Example: Run Codegen Agent directly
        print("\n--- Example: Run Codegen Agent Directly ---")
        result = await client.call_tool(
            "run_codegen_agent", 
            {
                "prompt": "Write a Python function to check if a string is a palindrome",
                "mock_mode": True
            }
        )
        print(f"Result: {result.text}")

if __name__ == "__main__":
    asyncio.run(main())

