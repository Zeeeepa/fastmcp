from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union
import uvicorn
import asyncio
import os
import json
from datetime import datetime
import uuid
from enum import Enum
from codegen import Agent

# Configuration
ORG_ID = os.getenv("ORG_ID", "323")
API_TOKEN = os.getenv("API_TOKEN", "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Model definitions
class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentRequest(BaseModel):
    context: str = Field(..., description="Agent input query or context text")
    additional_params: Optional[Dict[str, Any]] = Field(default={}, description="Additional parameters for the agent")

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: Optional[Any] = None
    created_at: str
    completed_at: Optional[str] = None
    endpoint: str

# Create FastAPI app
app = FastAPI(
    title="MCP Prompt Template Server",
    description="MCP server with 6 specialized prompt template endpoints",
    version="1.0.0"
)

# Task storage
tasks = {}

# Prompt templates
PROMPT_TEMPLATES = {
    "pr_creation": """[PR CREATION TEMPLATE]
You are tasked with creating a GitHub Pull Request based on the following details.

Instructions for PR creation:
- Create a clear, concise title that summarizes the changes
- Write a detailed description of the changes made
- Include relevant ticket/issue numbers
- List the key files modified and why
- Mention any breaking changes or migration notes
- Add appropriate labels and reviewers

Please analyze the following context and create a comprehensive PR:

{context}
""",
    
    "linear_issues": """[LINEAR ISSUE CREATION TEMPLATE]
You are tasked with creating a main Linear issue and appropriate sub-issues based on the following details.

Instructions for Linear issue creation:
- Create one main parent issue that encompasses the overall task
- Break down the work into multiple discrete sub-issues
- Each sub-issue should be clearly scoped with specific acceptance criteria
- Add appropriate labels, priority levels, and assignees
- Ensure dependencies between issues are clearly identified
- Set reasonable estimates for each issue

Please analyze the following context and create a comprehensive set of Linear issues:

{context}
""",
    
    "code_generation": """[CODE GENERATION TEMPLATE]
You are tasked with generating high-quality, optimized code based on the following specifications.

Instructions for code generation:
- Follow best practices and design patterns appropriate for the language
- Write clean, maintainable code with appropriate comments
- Consider edge cases and include error handling
- Optimize for performance where relevant
- Include usage examples and documentation

Please analyze the following context and generate the requested code:

{context}
""",
    
    "data_analysis": """[DATA ANALYSIS TEMPLATE]
You are tasked with analyzing data and providing meaningful insights based on the following details.

Instructions for data analysis:
- Understand the dataset structure and variables
- Identify key patterns, trends, and anomalies
- Apply appropriate statistical methods
- Visualize results effectively
- Provide actionable recommendations

Please analyze the following context and provide comprehensive data insights:

{context}
""",
    
    "documentation": """[DOCUMENTATION TEMPLATE]
You are tasked with creating comprehensive documentation based on the following details.

Instructions for documentation:
- Use clear, concise language
- Structure content logically with appropriate headings
- Include examples and use cases
- Define technical terms and concepts
- Consider the target audience's technical knowledge
- Include diagrams or visual aids when helpful

Please analyze the following context and create detailed documentation:

{context}
""",
    
    "testing_strategy": """[TESTING STRATEGY TEMPLATE]
You are tasked with developing a comprehensive testing strategy based on the following details.

Instructions for testing strategy:
- Identify appropriate testing types (unit, integration, e2e, etc.)
- Define test cases with clear expected outcomes
- Consider edge cases and failure scenarios
- Recommend testing tools and frameworks
- Outline test data requirements
- Include performance and security testing considerations

Please analyze the following context and develop a robust testing strategy:

{context}
"""
}

# Task execution functions
async def execute_agent_task(task_id: str, endpoint: str, context: str, additional_params: Dict[str, Any]):
    tasks[task_id]["status"] = TaskStatus.RUNNING
    
    try:
        # Get the appropriate template
        template = PROMPT_TEMPLATES.get(endpoint)
        if not template:
            raise ValueError(f"Unknown endpoint: {endpoint}")
        
        # Format the prompt with the agent's query context
        formatted_prompt = template.format(context=context)
        
        # Initialize the agent
        agent = Agent(org_id=ORG_ID, token=API_TOKEN)
        
        # Run the agent with the formatted prompt
        task = agent.run(formatted_prompt, **additional_params)
        
        # Check status periodically
        while True:
            task.refresh()
            if task.status == "completed":
                tasks[task_id]["status"] = TaskStatus.COMPLETED
                tasks[task_id]["result"] = task.result
                tasks[task_id]["completed_at"] = datetime.now().isoformat()
                break
            elif task.status == "failed":
                tasks[task_id]["status"] = TaskStatus.FAILED
                tasks[task_id]["result"] = {"error": "Agent task failed"}
                tasks[task_id]["completed_at"] = datetime.now().isoformat()
                break
            await asyncio.sleep(2)  # Poll every 2 seconds
            
    except Exception as e:
        tasks[task_id]["status"] = TaskStatus.FAILED
        tasks[task_id]["result"] = {"error": str(e)}
        tasks[task_id]["completed_at"] = datetime.now().isoformat()

# API Endpoints for each template
@app.post("/api/pr-creation", response_model=TaskResponse)
async def pr_creation_endpoint(request: AgentRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "result": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "endpoint": "pr_creation"
    }
    
    background_tasks.add_task(
        execute_agent_task,
        task_id=task_id,
        endpoint="pr_creation",
        context=request.context,
        additional_params=request.additional_params
    )
    
    return TaskResponse(**tasks[task_id])

@app.post("/api/linear-issues", response_model=TaskResponse)
async def linear_issues_endpoint(request: AgentRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "result": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "endpoint": "linear_issues"
    }
    
    background_tasks.add_task(
        execute_agent_task,
        task_id=task_id,
        endpoint="linear_issues",
        context=request.context,
        additional_params=request.additional_params
    )
    
    return TaskResponse(**tasks[task_id])

@app.post("/api/code-generation", response_model=TaskResponse)
async def code_generation_endpoint(request: AgentRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "result": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "endpoint": "code_generation"
    }
    
    background_tasks.add_task(
        execute_agent_task,
        task_id=task_id,
        endpoint="code_generation",
        context=request.context,
        additional_params=request.additional_params
    )
    
    return TaskResponse(**tasks[task_id])

@app.post("/api/data-analysis", response_model=TaskResponse)
async def data_analysis_endpoint(request: AgentRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "result": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "endpoint": "data_analysis"
    }
    
    background_tasks.add_task(
        execute_agent_task,
        task_id=task_id,
        endpoint="data_analysis",
        context=request.context,
        additional_params=request.additional_params
    )
    
    return TaskResponse(**tasks[task_id])

@app.post("/api/documentation", response_model=TaskResponse)
async def documentation_endpoint(request: AgentRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "result": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "endpoint": "documentation"
    }
    
    background_tasks.add_task(
        execute_agent_task,
        task_id=task_id,
        endpoint="documentation",
        context=request.context,
        additional_params=request.additional_params
    )
    
    return TaskResponse(**tasks[task_id])

@app.post("/api/testing-strategy", response_model=TaskResponse)
async def testing_strategy_endpoint(request: AgentRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "result": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "endpoint": "testing_strategy"
    }
    
    background_tasks.add_task(
        execute_agent_task,
        task_id=task_id,
        endpoint="testing_strategy",
        context=request.context,
        additional_params=request.additional_params
    )
    
    return TaskResponse(**tasks[task_id])

# Endpoint to check task status
@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskResponse(**tasks[task_id])

# Endpoint to list all tasks
@app.get("/api/tasks", response_model=List[TaskResponse])
async def list_tasks():
    return [TaskResponse(**task) for task in tasks.values()]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Run the server
if __name__ == "__main__":
    uvicorn.run("mcp_server:app", host="0.0.0.0", port=8000, reload=True)
