# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Codegen Agent MCP Server.

## Connection Issues

### Cannot Connect to Server

**Symptoms:**
- "Connection refused" error
- Timeout when trying to connect

**Possible Causes and Solutions:**

1. **Server not running**
   - Check if the server process is running
   - Restart the server: `python codegen_agent_server.py`

2. **Incorrect host or port**
   - Verify the host and port in your client code
   - Default is `http://127.0.0.1:8000/mcp`

3. **Firewall blocking connection**
   - Check firewall settings
   - Allow connections on port 8000

4. **Server crashed**
   - Check server logs for errors
   - Restart the server with more verbose logging: 
     ```python
     logging.basicConfig(level=logging.DEBUG)
     ```

## Authentication Issues

### Invalid Credentials

**Symptoms:**
- "Authentication failed" error
- "Invalid token" error

**Possible Causes and Solutions:**

1. **Incorrect organization ID or API token**
   - Verify your credentials
   - Check environment variables: `echo $CODEGEN_ORG_ID` and `echo $CODEGEN_TOKEN`
   - Try passing credentials directly in the API call

2. **Expired token**
   - Generate a new token from the Codegen dashboard
   - Update your environment variables or API calls

3. **Insufficient permissions**
   - Ensure your account has the necessary permissions
   - Contact your Codegen administrator

## Endpoint Issues

### Endpoint Not Found

**Symptoms:**
- "Endpoint not found" error
- "Unknown tool" error

**Possible Causes and Solutions:**

1. **Typo in endpoint name**
   - Check the spelling of the endpoint name
   - Use `client.list_tools()` to see available endpoints

2. **Server version mismatch**
   - Ensure you're using the correct server version
   - Update your server code

### Endpoint Returns Error

**Symptoms:**
- Error response from endpoint
- Task status is "failed" or "error"

**Possible Causes and Solutions:**

1. **Invalid query**
   - Check your query format
   - Simplify your query and try again

2. **Agent execution error**
   - Check the error message for details
   - Look at server logs for more information

3. **Rate limiting**
   - You might be making too many requests
   - Implement backoff and retry logic

## Template Issues

### Template Not Found

**Symptoms:**
- "Template not found" error

**Possible Causes and Solutions:**

1. **Typo in template name**
   - Check the spelling of the template name
   - Use `client.read_resource("prompts://templates")` to see available templates

2. **Custom template not added**
   - Ensure you've added the template to the `PROMPT_TEMPLATES` dictionary

### Template Formatting Issues

**Symptoms:**
- Unexpected agent behavior
- Missing information in agent output

**Possible Causes and Solutions:**

1. **Missing placeholders**
   - Ensure your template includes the `{agent_query}` placeholder
   - Check for typos in placeholder names

2. **Unclear instructions**
   - Make your template instructions more specific
   - Test with different queries

## Performance Issues

### Slow Response Times

**Symptoms:**
- Endpoints take a long time to respond
- Timeouts

**Possible Causes and Solutions:**

1. **Complex queries**
   - Simplify your queries
   - Break down complex tasks into smaller ones

2. **Server overload**
   - Check server resource usage
   - Consider scaling up your server

3. **Network latency**
   - Check your network connection
   - Consider deploying the server closer to your clients

## Debugging Techniques

### Enable Verbose Logging

Modify the logging configuration in `codegen_agent.py`:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Add Custom Logging

Add custom logging in the `run_codegen_agent` function:

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

### Check Server Status

You can add a health check endpoint to your server:

```python
@mcp.resource("health")
def health_check() -> Dict[str, str]:
    """
    Check if the server is running.
    
    Returns:
        A dictionary with the server status
    """
    return {"status": "ok"}
```

Then check it from your client:

```python
health = await client.read_resource("health")
print(f"Server status: {health.content['status']}")
```

### Test with Simplified Queries

If you're having issues, try testing with simplified queries to isolate the problem:

```python
result = await client.call_tool(
    "create_pr", 
    {
        "agent_query": "Create a simple PR"
    }
)
```

## Getting Help

If you're still having issues:

1. Check the [full documentation](codegen_agent_mcp_server.md)
2. Look for similar issues in the repository's issue tracker
3. Contact Codegen support with:
   - A description of the issue
   - Steps to reproduce
   - Error messages and logs
   - Your server and client code

