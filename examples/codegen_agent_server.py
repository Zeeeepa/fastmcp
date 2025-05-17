"""
Example of using the Codegen Agent MCP Server.

This script demonstrates how to create and run a Codegen Agent MCP Server.
"""

from fastmcp.contrib.codegen_agent import CodegenAgentServer

# Create the server
server = CodegenAgentServer(
    org_id="example-org-id",
    api_token="example-api-token",
    name="Codegen Agent Server",
    host="127.0.0.1",
    port=8000
)

# Configure the tools
server.configure_tools()

# Run the server with HTTP transport
if __name__ == "__main__":
    server.run(transport="streamable-http")

