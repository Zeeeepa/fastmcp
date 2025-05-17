# Codegen Agent MCP Server

This module provides a FastMCP server that integrates with the Codegen Agent API, offering 6 callable endpoints for different operations.

## Features

- FastMCP server with 6 callable endpoints for different Codegen Agent operations
- Prompt templates for each operation
- Resources for accessing prompt templates
- HTTP transport configuration

## Endpoints

The server provides the following endpoints:

1. `generate_code` - Generate code based on a description
2. `explain_code` - Explain existing code
3. `refactor_code` - Refactor code based on requirements
4. `fix_bug` - Fix bugs in code
5. `review_code` - Review code and provide feedback
6. `generate_documentation` - Generate documentation for code

## Usage

```python
from fastmcp.contrib.codegen_agent import CodegenAgentServer

# Create the server
server = CodegenAgentServer(
    org_id="your-org-id",
    api_token="your-api-token",
    name="Codegen Agent Server",
    host="127.0.0.1",
    port=8000
)

# Configure the tools
server.configure_tools()

# Run the server with HTTP transport
if __name__ == "__main__":
    server.run(transport="streamable-http")
```

## Prompt Templates

Each endpoint uses a specific prompt template:

- `code_generation` - Template for generating code
- `code_explanation` - Template for explaining code
- `code_refactoring` - Template for refactoring code
- `bug_fixing` - Template for fixing bugs
- `code_review` - Template for reviewing code
- `documentation` - Template for generating documentation

## Resources

The server provides resources for accessing prompt templates:

- `codegen://prompts` - Get all available prompt templates
- `codegen://prompts/{prompt_name}` - Get a specific prompt template

