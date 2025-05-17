"""
FastMCP Codegen Agent Server Example

This example demonstrates how to use the Codegen Agent API wrapper with FastMCP.
"""

import os
import asyncio
from typing import Dict, Any, Optional
from fastmcp import FastMCP, Context
from fastmcp.contrib.codegen_agent import CodegenAgent, Agent, TaskStatus

# Create server
mcp = FastMCP("Codegen Agent Example Server")

# Default credentials (would be configured via environment variables in production)
DEFAULT_ORG_ID = os.environ.get("CODEGEN_ORG_ID", "your-org-id")
DEFAULT_TOKEN = os.environ.get("CODEGEN_TOKEN", "your-api-token")

@mcp.tool()
async def run_codegen_agent(
    prompt: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None,
    mock_mode: bool = False
) -> Dict[str, Any]:
    """
    Run the Codegen Agent with the specified prompt.
    
    Args:
        prompt: The prompt to send to the agent
        ctx: The MCP context
        org_id: The organization ID (optional)
        token: The API token (optional)
        mock_mode: Whether to run in mock mode (for testing)
        
    Returns:
        The result of the agent execution
    """
    # Log the start of the agent execution
    await ctx.info(f"Starting Codegen Agent execution with prompt: {prompt[:100]}...")
    
    try:
        # Create a Codegen Agent
        agent = CodegenAgent(
            org_id=org_id or DEFAULT_ORG_ID,
            token=token or DEFAULT_TOKEN,
            mock_mode=mock_mode
        )
        
        # Run the agent
        await ctx.info("Agent is processing the request...")
        
        # Use the low-level API for more control and better status updates
        agent_client = Agent(
            org_id=org_id or DEFAULT_ORG_ID,
            token=token or DEFAULT_TOKEN,
            mock_mode=mock_mode
        )
        
        task = agent_client.run(prompt)
        
        # Poll for completion
        status_updates = ["⏳", "🔄", "⚙️", "📊", "🔍"]
        update_index = 0
        
        while task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.ERROR]:
            # Update status with a rotating indicator
            await ctx.info(f"{status_updates[update_index % len(status_updates)]} Task status: {task.status}")
            update_index += 1
            
            # Refresh the task status
            await task.refresh()
            
            # Wait before checking again
            await asyncio.sleep(1)
        
        # Check if the task completed successfully
        if task.status == TaskStatus.COMPLETED:
            await ctx.info("✅ Task completed successfully!")
            return {
                "status": "completed",
                "result": task.result
            }
        else:
            await ctx.error(f"❌ Task failed with status: {task.status}")
            return {
                "status": task.status,
                "error": task.error or "Unknown error"
            }
            
    except Exception as e:
        await ctx.error(f"❌ Error running Codegen Agent: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

@mcp.tool()
async def generate_code(
    description: str, 
    ctx: Context,
    language: str = "python",
    org_id: Optional[str] = None,
    token: Optional[str] = None,
    mock_mode: bool = True
) -> Dict[str, Any]:
    """
    Generate code based on a description.
    
    Args:
        description: The description of the code to generate
        language: The programming language to use
        ctx: The MCP context
        org_id: The organization ID (optional)
        token: The API token (optional)
        mock_mode: Whether to run in mock mode (for testing)
        
    Returns:
        The generated code
    """
    # Create a prompt for the Codegen Agent
    prompt = f"""
    Generate {language} code based on the following description:
    
    {description}
    
    Please provide only the code without any explanations or comments.
    """
    
    # Run the Codegen Agent
    return await run_codegen_agent(
        prompt=prompt,
        ctx=ctx,
        org_id=org_id,
        token=token,
        mock_mode=mock_mode
    )

@mcp.tool()
async def explain_code(
    code: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None,
    mock_mode: bool = True
) -> Dict[str, Any]:
    """
    Explain the provided code.
    
    Args:
        code: The code to explain
        ctx: The MCP context
        org_id: The organization ID (optional)
        token: The API token (optional)
        mock_mode: Whether to run in mock mode (for testing)
        
    Returns:
        The explanation of the code
    """
    # Create a prompt for the Codegen Agent
    prompt = f"""
    Explain the following code:
    
    ```
    {code}
    ```
    
    Please provide a detailed explanation of what the code does and how it works.
    """
    
    # Run the Codegen Agent
    return await run_codegen_agent(
        prompt=prompt,
        ctx=ctx,
        org_id=org_id,
        token=token,
        mock_mode=mock_mode
    )

# Run the server if this file is executed directly
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)

