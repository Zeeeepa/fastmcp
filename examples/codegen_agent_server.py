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
import logging
from pathlib import Path

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not installed, skipping .env file loading")
except Exception as e:
    print(f"Error loading .env file: {e}")

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

# Server configuration
MCP_HOST = os.environ.get("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.environ.get("MCP_PORT", "8000"))

# Configure logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add a health check endpoint
@mcp.resource("health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring.
    
    Returns:
        A dictionary with the server status
    """
    return {"status": "healthy"}

# Run the server if this file is executed directly
if __name__ == "__main__":
    logger.info(f"Starting Codegen Agent MCP Server on {MCP_HOST}:{MCP_PORT}")
    mcp.run(transport="streamable-http", host=MCP_HOST, port=MCP_PORT)
