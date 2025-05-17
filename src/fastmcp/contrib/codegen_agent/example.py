"""
Example usage of the Codegen Agent API wrapper.
"""

import asyncio
import os
from .agent import CodegenAgent, Agent, CodegenTask, TaskStatus

async def run_agent_example():
    """
    Example of using the CodegenAgent class.
    """
    # Get credentials from environment variables or use defaults
    org_id = os.environ.get("CODEGEN_ORG_ID", "your-org-id")
    token = os.environ.get("CODEGEN_TOKEN", "your-api-token")
    
    # Create a Codegen Agent
    agent = CodegenAgent(org_id=org_id, token=token, mock_mode=True)
    
    # Run the agent with a prompt
    result = await agent.run("Create a simple Python function to calculate the factorial of a number")
    
    # Print the result
    print(f"Status: {result['status']}")
    if result['status'] == "completed":
        print(f"Result: {result['result']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")

async def run_low_level_example():
    """
    Example of using the low-level Agent class.
    """
    # Get credentials from environment variables or use defaults
    org_id = os.environ.get("CODEGEN_ORG_ID", "your-org-id")
    token = os.environ.get("CODEGEN_TOKEN", "your-api-token")
    
    # Create an Agent
    agent = Agent(org_id=org_id, token=token, mock_mode=True)
    
    # Run the agent with a prompt
    task = agent.run("Create a simple Python function to calculate the factorial of a number")
    
    # Poll for completion
    status_updates = ["⏳", "🔄", "⚙️", "📊", "🔍"]
    update_index = 0
    
    while task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.ERROR]:
        # Update status with a rotating indicator
        print(f"{status_updates[update_index % len(status_updates)]} Task status: {task.status}")
        update_index += 1
        
        # Refresh the task status
        await task.refresh()
        
        # Wait before checking again
        await asyncio.sleep(1)
    
    # Check if the task completed successfully
    if task.status == TaskStatus.COMPLETED:
        print("✅ Task completed successfully!")
        print(f"Result: {task.result}")
    else:
        print(f"❌ Task failed with status: {task.status}")
        print(f"Error: {task.error or 'Unknown error'}")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(run_agent_example())
    print("\n" + "-" * 50 + "\n")
    asyncio.run(run_low_level_example())

