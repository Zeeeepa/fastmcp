#!/usr/bin/env python3
"""
Codegen Agent MCP Client Example

This example demonstrates how to use the Codegen Agent MCP server.
It covers:
- Connecting to the MCP server
- Listing available tools and prompt templates
- Calling each endpoint with example queries
- Handling errors properly

Usage:
    python codegen_agent_client_example.py [--host HOST] [--port PORT]

Options:
    --host HOST    Server host (default: 127.0.0.1)
    --port PORT    Server port (default: 8000)
"""

import asyncio
import json
import argparse
import sys
from typing import Dict, Any, List, Optional
from fastmcp import Client, Resource, ToolResponse

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")

def print_section(text: str) -> None:
    """Print a formatted section header."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'-' * len(text)}{Colors.ENDC}")

def print_success(text: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}{text}{Colors.ENDC}")

def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}{Colors.BOLD}ERROR: {text}{Colors.ENDC}")

def print_warning(text: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}WARNING: {text}{Colors.ENDC}")

def print_info(text: str) -> None:
    """Print an info message."""
    print(f"{Colors.CYAN}{text}{Colors.ENDC}")

def format_json(data: Any) -> str:
    """Format JSON data for display."""
    return json.dumps(data, indent=2)

async def connect_to_server(host: str, port: int) -> Client:
    """
    Connect to the MCP server.
    
    Args:
        host: The server host
        port: The server port
        
    Returns:
        A connected MCP client
        
    Raises:
        ConnectionError: If the connection fails
    """
    url = f"http://{host}:{port}/mcp"
    print_info(f"Connecting to MCP server at {url}...")
    
    try:
        client = Client(url)
        await client.connect()
        print_success(f"Successfully connected to MCP server at {url}")
        return client
    except Exception as e:
        print_error(f"Failed to connect to MCP server: {str(e)}")
        raise ConnectionError(f"Could not connect to MCP server at {url}: {str(e)}")

async def list_tools(client: Client) -> List[Dict[str, Any]]:
    """
    List all available tools on the server.
    
    Args:
        client: The MCP client
        
    Returns:
        A list of available tools
    """
    print_section("Available Tools")
    
    try:
        tools = await client.list_tools()
        
        if not tools:
            print_warning("No tools available on the server")
            return []
            
        print(f"Found {len(tools)} available tools:")
        for i, tool in enumerate(tools, 1):
            print(f"{i}. {Colors.BOLD}{tool['name']}{Colors.ENDC}: {tool['description']}")
            print(f"   Parameters: {format_json(tool.get('parameters', {}))}")
            print()
            
        return tools
    except Exception as e:
        print_error(f"Failed to list tools: {str(e)}")
        return []

async def list_prompt_templates(client: Client) -> Dict[str, str]:
    """
    List all available prompt templates.
    
    Args:
        client: The MCP client
        
    Returns:
        A dictionary of prompt templates
    """
    print_section("Available Prompt Templates")
    
    try:
        resource = await client.read_resource("prompts://templates")
        templates = resource.content
        
        if not templates:
            print_warning("No prompt templates available")
            return {}
            
        print(f"Found {len(templates)} prompt templates:")
        for name, template in templates.items():
            print(f"- {Colors.BOLD}{name}{Colors.ENDC}")
            print(f"  {template[:100]}..." if len(template) > 100 else f"  {template}")
            print()
            
        return templates
    except Exception as e:
        print_error(f"Failed to list prompt templates: {str(e)}")
        return {}

async def call_tool(client: Client, tool_name: str, params: Dict[str, Any]) -> Optional[ToolResponse]:
    """
    Call a tool with the given parameters.
    
    Args:
        client: The MCP client
        tool_name: The name of the tool to call
        params: The parameters to pass to the tool
        
    Returns:
        The tool response, or None if the call failed
    """
    print_section(f"Calling Tool: {tool_name}")
    print_info(f"Parameters: {format_json(params)}")
    
    try:
        result = await client.call_tool(tool_name, params)
        print_success("Tool call successful!")
        print(f"Response: {result.text}")
        return result
    except Exception as e:
        print_error(f"Tool call failed: {str(e)}")
        return None

async def demonstrate_error_handling(client: Client) -> None:
    """
    Demonstrate error handling with invalid requests.
    
    Args:
        client: The MCP client
    """
    print_section("Error Handling Demonstration")
    
    # Case 1: Call a non-existent tool
    print_info("Attempting to call a non-existent tool...")
    try:
        await client.call_tool("non_existent_tool", {"param": "value"})
        print_warning("Expected an error, but the call succeeded!")
    except Exception as e:
        print_success(f"Correctly handled error: {str(e)}")
    
    # Case 2: Call a tool with missing required parameters
    print_info("\nAttempting to call a tool with missing required parameters...")
    try:
        await client.call_tool("create_pr", {})
        print_warning("Expected an error, but the call succeeded!")
    except Exception as e:
        print_success(f"Correctly handled error: {str(e)}")
    
    # Case 3: Call a tool with invalid parameters
    print_info("\nAttempting to call a tool with invalid parameters...")
    try:
        await client.call_tool("create_pr", {"agent_query": 123})  # agent_query should be a string
        print_warning("Expected an error, but the call succeeded!")
    except Exception as e:
        print_success(f"Correctly handled error: {str(e)}")

async def main() -> None:
    """Main function to demonstrate the client usage."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Codegen Agent MCP Client Example")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    args = parser.parse_args()
    
    print_header("Codegen Agent MCP Client Example")
    
    try:
        # Connect to the server
        client = await connect_to_server(args.host, args.port)
        
        # List available tools
        tools = await list_tools(client)
        
        # List available prompt templates
        templates = await list_prompt_templates(client)
        
        if not tools or not templates:
            print_error("Cannot proceed without tools and templates")
            return
        
        # Demonstrate calling each endpoint
        tool_examples = {
            "create_pr": {
                "agent_query": "Create a PR that adds a new feature to calculate the factorial of a number"
            },
            "create_linear_issues": {
                "agent_query": "Create a main issue for implementing a new authentication system with sub-issues for login, registration, password reset, and user profile management"
            },
            "analyze_codebase": {
                "agent_query": "Analyze the codebase for performance bottlenecks and security vulnerabilities"
            },
            "fix_bug": {
                "agent_query": "Fix the bug where the login form doesn't validate email addresses correctly"
            },
            "review_pr": {
                "agent_query": "Review PR #123 that adds a new user profile page"
            },
            "generate_documentation": {
                "agent_query": "Generate comprehensive documentation for the authentication module"
            }
        }
        
        # Call each tool with example parameters
        for tool_name, params in tool_examples.items():
            await call_tool(client, tool_name, params)
            print()  # Add a blank line between tool calls
        
        # Demonstrate error handling
        await demonstrate_error_handling(client)
        
        print_header("Client Example Completed Successfully")
        
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        sys.exit(1)
    finally:
        # Ensure the client is closed properly
        if 'client' in locals():
            await client.close()
            print_info("Client connection closed")

if __name__ == "__main__":
    asyncio.run(main())

