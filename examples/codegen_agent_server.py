"""
FastMCP Codegen Agent Server

This server provides 6 callable endpoints that integrate with the Codegen Agent.
Each endpoint executes the same function with different prompt templates.

Endpoints:
1. create_pr - Creates a PR with the specified changes
2. create_linear_issues - Creates a main issue and sub-issues in Linear
3. analyze_codebase - Analyzes a codebase and provides insights
4. fix_bug - Fixes a bug in the codebase
5. review_pr - Reviews a PR and provides feedback
6. generate_documentation - Generates documentation for a codebase
"""

import os
import asyncio
from typing import Dict, Any, Optional
from fastmcp import FastMCP, Context

# Import our Codegen Agent module
# In a real implementation, this would be:
# from codegen import Agent
# For now, we'll use our mock implementation
from codegen_agent import Agent

# Create server
mcp = FastMCP("Codegen Agent Server")

# Default credentials (would be configured via environment variables in production)
DEFAULT_ORG_ID = os.environ.get("CODEGEN_ORG_ID", "323")
DEFAULT_TOKEN = os.environ.get("CODEGEN_TOKEN", "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Define the prompt templates
PROMPT_TEMPLATES = {
    "create_pr": """
    Create a PR with the following specifications:
    
    {agent_query}
    
    Instructions:
    - Create a new branch from the main branch
    - Make the necessary changes
    - Create a PR with a descriptive title and body
    - Link any relevant issues
    """,
    
    "create_linear_issues": """
    Create a main issue and sub-issues in Linear with the following specifications:
    
    {agent_query}
    
    Instructions:
    - Create a main issue with a descriptive title and body
    - Create sub-issues for each discrete functionality
    - Link the sub-issues to the main issue
    - Assign appropriate labels and priorities
    """,
    
    "analyze_codebase": """
    Analyze the codebase and provide insights:
    
    {agent_query}
    
    Instructions:
    - Analyze the structure of the codebase
    - Identify potential issues or areas for improvement
    - Provide recommendations for best practices
    - Suggest optimizations if applicable
    """,
    
    "fix_bug": """
    Fix the bug in the codebase:
    
    {agent_query}
    
    Instructions:
    - Identify the root cause of the bug
    - Implement a fix
    - Add tests to prevent regression
    - Create a PR with the fix
    """,
    
    "review_pr": """
    Review the PR and provide feedback:
    
    {agent_query}
    
    Instructions:
    - Review the code changes
    - Check for potential issues or bugs
    - Suggest improvements
    - Provide constructive feedback
    """,
    
    "generate_documentation": """
    Generate documentation for the codebase:
    
    {agent_query}
    
    Instructions:
    - Analyze the codebase structure
    - Generate comprehensive documentation
    - Include usage examples
    - Explain key concepts and components
    """
}

async def run_codegen_agent(
    prompt_template: str, 
    agent_query: str, 
    ctx: Context,
    org_id: str = DEFAULT_ORG_ID,
    token: str = DEFAULT_TOKEN
) -> Dict[str, Any]:
    """
    Run the Codegen Agent with the specified prompt template and agent query.
    
    Args:
        prompt_template: The prompt template to use
        agent_query: The agent query to include in the prompt
        ctx: The MCP context
        org_id: The organization ID (optional)
        token: The API token (optional)
        
    Returns:
        The result of the agent execution
    """
    # Log the start of the agent execution
    await ctx.info(f"Starting Codegen Agent execution with template: {prompt_template}")
    
    # Format the prompt with the agent query
    formatted_prompt = PROMPT_TEMPLATES[prompt_template].format(agent_query=agent_query)
    
    # Log the formatted prompt
    await ctx.info("Executing agent with the following prompt:")
    await ctx.info(formatted_prompt[:200] + "..." if len(formatted_prompt) > 200 else formatted_prompt)
    
    try:
        # Create an agent
        agent = Agent(org_id=org_id, token=token)
        
        # Run the task
        await ctx.info("Agent is processing the request...")
        task = agent.run(formatted_prompt)
        
        # Poll for completion
        status_updates = ["⏳", "🔄", "⚙️", "📊", "🔍"]
        update_index = 0
        
        while task.status not in ["completed", "failed", "error"]:
            # Update status with a rotating indicator
            await ctx.info(f"{status_updates[update_index % len(status_updates)]} Task status: {task.status}")
            update_index += 1
            
            # Refresh the task status
            task.refresh()
            
            # Wait before checking again
            await asyncio.sleep(1)
        
        # Check if the task completed successfully
        if task.status == "completed":
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
async def create_pr(
    agent_query: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a PR with the specified changes.
    
    Args:
        agent_query: The query describing what changes to make and PR details
        org_id: The organization ID (optional)
        token: The API token (optional)
        
    Returns:
        The result of the PR creation
    """
    return await run_codegen_agent(
        "create_pr", 
        agent_query, 
        ctx,
        org_id or DEFAULT_ORG_ID,
        token or DEFAULT_TOKEN
    )

@mcp.tool()
async def create_linear_issues(
    agent_query: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a main issue and sub-issues in Linear.
    
    Args:
        agent_query: The query describing the issues to create
        org_id: The organization ID (optional)
        token: The API token (optional)
        
    Returns:
        The result of the issue creation
    """
    return await run_codegen_agent(
        "create_linear_issues", 
        agent_query, 
        ctx,
        org_id or DEFAULT_ORG_ID,
        token or DEFAULT_TOKEN
    )

@mcp.tool()
async def analyze_codebase(
    agent_query: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze a codebase and provide insights.
    
    Args:
        agent_query: The query describing what to analyze
        org_id: The organization ID (optional)
        token: The API token (optional)
        
    Returns:
        The analysis results
    """
    return await run_codegen_agent(
        "analyze_codebase", 
        agent_query, 
        ctx,
        org_id or DEFAULT_ORG_ID,
        token or DEFAULT_TOKEN
    )

@mcp.tool()
async def fix_bug(
    agent_query: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fix a bug in the codebase.
    
    Args:
        agent_query: The query describing the bug to fix
        org_id: The organization ID (optional)
        token: The API token (optional)
        
    Returns:
        The result of the bug fix
    """
    return await run_codegen_agent(
        "fix_bug", 
        agent_query, 
        ctx,
        org_id or DEFAULT_ORG_ID,
        token or DEFAULT_TOKEN
    )

@mcp.tool()
async def review_pr(
    agent_query: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Review a PR and provide feedback.
    
    Args:
        agent_query: The query describing the PR to review
        org_id: The organization ID (optional)
        token: The API token (optional)
        
    Returns:
        The review results
    """
    return await run_codegen_agent(
        "review_pr", 
        agent_query, 
        ctx,
        org_id or DEFAULT_ORG_ID,
        token or DEFAULT_TOKEN
    )

@mcp.tool()
async def generate_documentation(
    agent_query: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate documentation for a codebase.
    
    Args:
        agent_query: The query describing what documentation to generate
        org_id: The organization ID (optional)
        token: The API token (optional)
        
    Returns:
        The generated documentation
    """
    return await run_codegen_agent(
        "generate_documentation", 
        agent_query, 
        ctx,
        org_id or DEFAULT_ORG_ID,
        token or DEFAULT_TOKEN
    )

# Add resources for the prompt templates
@mcp.resource("prompts://templates")
def get_prompt_templates() -> Dict[str, str]:
    """
    Get all available prompt templates.
    
    Returns:
        A dictionary of prompt templates
    """
    return PROMPT_TEMPLATES

@mcp.resource("prompts://templates/{template_name}")
def get_prompt_template(template_name: str) -> str:
    """
    Get a specific prompt template.
    
    Args:
        template_name: The name of the template to retrieve
        
    Returns:
        The prompt template
    """
    if template_name not in PROMPT_TEMPLATES:
        raise ValueError(f"Template '{template_name}' not found")
    return PROMPT_TEMPLATES[template_name]

# Run the server if this file is executed directly
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)

