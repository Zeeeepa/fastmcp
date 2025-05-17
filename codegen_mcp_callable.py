"""
MCP Python Callable Server with 6 specialized endpoints.

This module provides a simple interface to execute Codegen Agent tasks
with specialized prompt templates for different use cases.
"""

import os
from typing import Dict, Any, Optional, Union, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import the Codegen SDK, use mock if not available
try:
    from codegen import Agent
except ImportError:
    print("Codegen SDK not found. Please install it with: pip install codegen")
    print("For now, we'll use a mock implementation for demonstration purposes.")
    from mock_codegen import Agent

# Configuration
ORG_ID = os.getenv("ORG_ID", "323")
API_TOKEN = os.getenv("API_TOKEN", "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

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
- Include examples and code snippets where relevant
- Address different user levels (beginners to advanced)
- Consider both reference and tutorial aspects

Please analyze the following context and create comprehensive documentation:

{context}
""",
    
    "testing_strategy": """[TESTING STRATEGY TEMPLATE]
You are tasked with developing a testing strategy based on the following details.

Instructions for testing strategy:
- Identify key test scenarios and edge cases
- Recommend appropriate testing levels (unit, integration, e2e)
- Suggest testing frameworks and tools
- Consider performance and security testing needs
- Outline validation criteria for success

Please analyze the following context and develop a comprehensive testing strategy:

{context}
"""
}

class CodegenMCPCallable:
    """
    A class that provides callable endpoints for the Codegen Agent with specialized prompt templates.
    """
    
    def __init__(self, org_id: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize the CodegenMCPCallable with organization ID and API token.
        
        Args:
            org_id: The organization ID for Codegen API
            token: The API token for Codegen API
        """
        self.org_id = org_id or ORG_ID
        self.token = token or API_TOKEN
        self.agent = Agent(org_id=self.org_id, token=self.token)
    
    def _execute_template(self, template_key: str, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a template with the given context.
        
        Args:
            template_key: The key of the template to use
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            The result of the agent task
        """
        if template_key not in PROMPT_TEMPLATES:
            raise ValueError(f"Unknown template key: {template_key}")
        
        # Format the prompt with the context
        prompt = PROMPT_TEMPLATES[template_key].format(context=context)
        
        # Add additional parameters if provided
        if additional_params:
            prompt += f"\n\nAdditional Parameters: {additional_params}"
        
        # Run the agent task
        task = self.agent.run(prompt)
        
        # Refresh to get updated status
        task.refresh()
        
        # Return the result if completed
        if task.status == "completed":
            return task.result
        
        return {"status": task.status, "message": "Task not completed yet"}
    
    def create_pr(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute PR creation template with the given context.
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            The result of the agent task
        """
        return self._execute_template("pr_creation", context, additional_params)
    
    def create_linear_issues(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute Linear issues template with the given context.
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            The result of the agent task
        """
        return self._execute_template("linear_issues", context, additional_params)
    
    def generate_code(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute code generation template with the given context.
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            The result of the agent task
        """
        return self._execute_template("code_generation", context, additional_params)
    
    def analyze_data(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute data analysis template with the given context.
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            The result of the agent task
        """
        return self._execute_template("data_analysis", context, additional_params)
    
    def create_documentation(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute documentation template with the given context.
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            The result of the agent task
        """
        return self._execute_template("documentation", context, additional_params)
    
    def create_testing_strategy(self, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute testing strategy template with the given context.
        
        Args:
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            The result of the agent task
        """
        return self._execute_template("testing_strategy", context, additional_params)

# Example usage
if __name__ == "__main__":
    # Create an instance of CodegenMCPCallable
    mcp = CodegenMCPCallable()
    
    # Example: Create a PR
    result = mcp.create_pr(
        context="Create a pull request for adding user authentication features. The changes include new login/logout endpoints, JWT token handling, and user session management."
    )
    
    print(f"Result: {result}")

