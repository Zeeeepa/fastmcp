# Codegen Agent MCP Client Example

This example demonstrates how to use the Codegen Agent MCP server from a client application. It provides a comprehensive example of connecting to the server, listing available tools and prompt templates, calling each endpoint with example queries, and handling errors properly.

## Features

- Connect to the Codegen Agent MCP server
- List all available tools and their parameters
- List all available prompt templates
- Call each endpoint with example queries
- Demonstrate proper error handling
- Colorized terminal output for better readability

## Prerequisites

- Python 3.7+
- `fastmcp` package installed
- Running Codegen Agent MCP server (see [Codegen Agent MCP Server README](./codegen_agent_README.md))

## Installation

```bash
# Install the required package
pip install fastmcp
```

## Usage

```bash
# Run with default settings (connects to server at http://127.0.0.1:8000/mcp)
python codegen_agent_client_example.py

# Specify a different host and port
python codegen_agent_client_example.py --host 192.168.1.100 --port 8080
```

## Command Line Options

- `--host HOST`: Server host (default: 127.0.0.1)
- `--port PORT`: Server port (default: 8000)

## Example Output

When you run the client example, you'll see output similar to the following:

```
============================================================
            Codegen Agent MCP Client Example            
============================================================

Connecting to MCP server at http://127.0.0.1:8000/mcp...
Successfully connected to MCP server at http://127.0.0.1:8000/mcp

Available Tools
--------------
Found 6 available tools:
1. create_pr: Create a PR with the specified changes.
   Parameters: {...}

2. create_linear_issues: Create a main issue and sub-issues in Linear.
   Parameters: {...}

...

Available Prompt Templates
-------------------------
Found 6 prompt templates:
- create_pr
  Create a PR with the following specifications:...

- create_linear_issues
  Create a main issue and sub-issues in Linear with the following specifications:...

...

Calling Tool: create_pr
----------------------
Parameters: {
  "agent_query": "Create a PR that adds a new feature to calculate the factorial of a number"
}
Tool call successful!
Response: {"status": "completed", "result": "Simulated result for prompt: Create a PR that adds a new feature to calculate the..."}

...

Error Handling Demonstration
---------------------------
Attempting to call a non-existent tool...
Correctly handled error: Tool 'non_existent_tool' not found

...

============================================================
        Client Example Completed Successfully            
============================================================

Client connection closed
```

## Key Components

### Connection Management

The client example demonstrates proper connection management, including:

- Establishing a connection to the server
- Handling connection errors
- Properly closing the connection when done

```python
# Connect to the server
client = await connect_to_server(host, port)

# ... use the client ...

# Close the connection when done
await client.close()
```

### Tool Discovery

The example shows how to discover available tools on the server:

```python
# List available tools
tools = await client.list_tools()
```

### Resource Access

The example demonstrates how to access resources provided by the server:

```python
# Get available prompt templates
templates = await client.read_resource("prompts://templates")
```

### Tool Invocation

The example shows how to call tools with parameters:

```python
# Call a tool
result = await client.call_tool("tool_name", {"param1": "value1"})
```

### Error Handling

The example demonstrates proper error handling for various scenarios:

- Connection errors
- Non-existent tools
- Missing required parameters
- Invalid parameter types

## Customization

You can customize the example to fit your specific needs:

- Add additional tool calls with different parameters
- Implement more sophisticated error handling
- Add authentication if your server requires it
- Extend the client to handle streaming responses

## Integration with Your Application

To integrate the Codegen Agent MCP client into your application:

1. Import the necessary components:
   ```python
   from fastmcp import Client
   ```

2. Create a client and connect to the server:
   ```python
   client = Client("http://your-server:port/mcp")
   await client.connect()
   ```

3. Call tools as needed:
   ```python
   result = await client.call_tool("tool_name", {"param1": "value1"})
   ```

4. Close the connection when done:
   ```python
   await client.close()
   ```

## Error Handling Best Practices

When integrating with the Codegen Agent MCP server, follow these error handling best practices:

1. **Connection Errors**: Handle connection errors gracefully, with appropriate retries if necessary.

2. **Tool Errors**: Catch exceptions when calling tools and provide meaningful error messages.

3. **Parameter Validation**: Validate parameters before sending them to the server to catch errors early.

4. **Resource Errors**: Handle errors when accessing resources, such as non-existent resources.

5. **Timeouts**: Implement timeouts for long-running operations to prevent hanging.

## Related Resources

- [Codegen Agent MCP Server README](./codegen_agent_README.md)
- [FastMCP Documentation](https://github.com/Zeeeepa/fastmcp)

