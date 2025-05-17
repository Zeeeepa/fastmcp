"""
MCP Python Callable Server with 6 specialized endpoints.

This module provides a simple interface to execute Codegen Agent tasks
with specialized prompt templates for different use cases.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, Union, List, Tuple
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import the Codegen SDK
try:
    from codegen import Agent
    logger.info("Successfully imported Codegen SDK")
except ImportError as e:
    logger.error(f"Failed to import Codegen SDK: {e}")
    raise ImportError("Codegen SDK not found. Please install it with: pip install codegen")

# Configuration
ORG_ID = os.getenv("ORG_ID", "323")
API_TOKEN = os.getenv("API_TOKEN", "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "300"))  # 5 minutes default timeout

# Prompt templates
PR_CREATION_TEMPLATE = """[PR CREATION TEMPLATE]
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
"""

LINEAR_ISSUES_TEMPLATE = """[LINEAR ISSUE CREATION TEMPLATE]
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
"""

CODE_GENERATION_TEMPLATE = """[CODE GENERATION TEMPLATE]
You are tasked with generating high-quality, optimized code based on the following specifications.

Instructions for code generation:
- Follow best practices and design patterns appropriate for the language
- Write clean, maintainable code with appropriate comments
- Consider edge cases and include error handling
- Optimize for performance where relevant
- Include usage examples and documentation

Please analyze the following context and generate the requested code:

{context}
"""

DATA_ANALYSIS_TEMPLATE = """[DATA ANALYSIS TEMPLATE]
You are tasked with analyzing data and providing meaningful insights based on the following details.

Instructions for data analysis:
- Understand the dataset structure and variables
- Identify key patterns, trends, and anomalies
- Apply appropriate statistical methods
- Visualize results effectively
- Provide actionable recommendations

Please analyze the following context and provide comprehensive data insights:

{context}
"""

DOCUMENTATION_TEMPLATE = """[DOCUMENTATION TEMPLATE]
You are tasked with creating comprehensive documentation based on the following details.

Instructions for documentation:
- Use clear, concise language
- Structure content logically with appropriate headings
- Include examples and code snippets where relevant
- Address different user levels (beginners to advanced)
- Consider both reference and tutorial aspects

Please analyze the following context and create comprehensive documentation:

{context}
"""

TESTING_STRATEGY_TEMPLATE = """[TESTING STRATEGY TEMPLATE]
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

class CodegenMCPCallable:
    """
    A class that provides callable endpoints for the Codegen Agent with specialized prompt templates.
    """
    
    def __init__(self, org_id: Optional[str] = None, token: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the CodegenMCPCallable with organization ID and API token.
        
        Args:
            org_id: The organization ID for Codegen API
            token: The API token for Codegen API
            timeout: The timeout in seconds for agent tasks
        """
        self.org_id = org_id or ORG_ID
        self.token = token or API_TOKEN
        self.timeout = timeout or DEFAULT_TIMEOUT
        
        logger.info(f"Initializing CodegenMCPCallable with org_id={self.org_id}, timeout={self.timeout}")
        
        try:
            self.agent = Agent(org_id=self.org_id, token=self.token)
            logger.info("Successfully initialized Codegen Agent")
        except Exception as e:
            logger.error(f"Failed to initialize Codegen Agent: {e}")
            raise
        
        # Store templates
        self.templates = {
            "pr_creation": PR_CREATION_TEMPLATE,
            "linear_issues": LINEAR_ISSUES_TEMPLATE,
            "code_generation": CODE_GENERATION_TEMPLATE,
            "data_analysis": DATA_ANALYSIS_TEMPLATE,
            "documentation": DOCUMENTATION_TEMPLATE,
            "testing_strategy": TESTING_STRATEGY_TEMPLATE
        }
        
        # Store task history
        self.task_history = []
    
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
        if template_key not in self.templates:
            error_msg = f"Unknown template key: {template_key}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Format the prompt with the context
        prompt = self.templates[template_key].format(context=context)
        
        # Add additional parameters if provided
        if additional_params:
            prompt += f"\n\nAdditional Parameters: {json.dumps(additional_params, indent=2)}"
        
        # Log the task execution
        logger.info(f"Executing template '{template_key}' with context length {len(context)}")
        
        try:
            # Run the agent task
            task = self.agent.run(prompt)
            task_id = getattr(task, 'id', 'unknown')
            
            # Store task in history
            task_info = {
                'task_id': task_id,
                'template_key': template_key,
                'context_length': len(context),
                'timestamp': None,  # Will be updated when task completes
                'status': 'pending'
            }
            self.task_history.append(task_info)
            
            # Wait for task to complete with timeout
            import time
            start_time = time.time()
            
            while time.time() - start_time < self.timeout:
                # Refresh to get updated status
                task.refresh()
                
                if task.status == "completed":
                    # Update task history
                    task_info['status'] = 'completed'
                    task_info['timestamp'] = time.time()
                    logger.info(f"Task {task_id} completed successfully")
                    return task.result
                
                if task.status == "failed":
                    # Update task history
                    task_info['status'] = 'failed'
                    task_info['timestamp'] = time.time()
                    error_msg = f"Task {task_id} failed with status: {task.status}"
                    logger.error(error_msg)
                    return {"status": "failed", "message": error_msg}
                
                # Sleep for a short time before checking again
                time.sleep(2)
            
            # If we get here, the task timed out
            task_info['status'] = 'timeout'
            task_info['timestamp'] = time.time()
            error_msg = f"Task {task_id} timed out after {self.timeout} seconds"
            logger.error(error_msg)
            return {"status": "timeout", "message": error_msg}
            
        except Exception as e:
            logger.error(f"Error executing template '{template_key}': {e}")
            return {"status": "error", "message": str(e)}
    
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
    
    def get_template(self, template_key: str) -> str:
        """
        Get the template for a specific key.
        
        Args:
            template_key: The key of the template to get
            
        Returns:
            The template string
        """
        if template_key not in self.templates:
            error_msg = f"Unknown template key: {template_key}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return self.templates[template_key]
    
    def set_template(self, template_key: str, template: str) -> None:
        """
        Set or update a template.
        
        Args:
            template_key: The key of the template to set
            template: The template string
        """
        logger.info(f"Setting template '{template_key}' with length {len(template)}")
        self.templates[template_key] = template
    
    def add_template(self, template_key: str, template: str) -> None:
        """
        Add a new template.
        
        Args:
            template_key: The key of the new template
            template: The template string
        """
        if template_key in self.templates:
            error_msg = f"Template key '{template_key}' already exists. Use set_template to update it."
            logger.warning(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Adding new template '{template_key}' with length {len(template)}")
        self.templates[template_key] = template
    
    def delete_template(self, template_key: str) -> None:
        """
        Delete a template.
        
        Args:
            template_key: The key of the template to delete
        """
        if template_key not in self.templates:
            error_msg = f"Unknown template key: {template_key}"
            logger.warning(error_msg)
            raise ValueError(error_msg)
        
        # Don't allow deletion of default templates
        default_templates = ["pr_creation", "linear_issues", "code_generation", 
                            "data_analysis", "documentation", "testing_strategy"]
        if template_key in default_templates:
            error_msg = f"Cannot delete default template: {template_key}"
            logger.warning(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Deleting template '{template_key}'")
        del self.templates[template_key]
    
    def list_templates(self) -> Dict[str, str]:
        """
        List all available templates.
        
        Returns:
            A dictionary of template keys and their values
        """
        return self.templates
    
    def get_task_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of executed tasks.
        
        Returns:
            A list of task history entries
        """
        return self.task_history
    
    def clear_task_history(self) -> None:
        """
        Clear the task history.
        """
        logger.info("Clearing task history")
        self.task_history = []
    
    def execute_custom_template(self, template: str, context: str, additional_params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a custom template with the given context.
        
        Args:
            template: The custom template to use
            context: The context text to be processed by the agent
            additional_params: Additional parameters for the agent
            
        Returns:
            The result of the agent task
        """
        # Format the prompt with the context
        prompt = template.format(context=context)
        
        # Add additional parameters if provided
        if additional_params:
            prompt += f"\n\nAdditional Parameters: {json.dumps(additional_params, indent=2)}"
        
        # Log the task execution
        logger.info(f"Executing custom template with context length {len(context)}")
        
        try:
            # Run the agent task
            task = self.agent.run(prompt)
            task_id = getattr(task, 'id', 'unknown')
            
            # Store task in history
            task_info = {
                'task_id': task_id,
                'template_key': 'custom',
                'context_length': len(context),
                'timestamp': None,  # Will be updated when task completes
                'status': 'pending'
            }
            self.task_history.append(task_info)
            
            # Wait for task to complete with timeout
            import time
            start_time = time.time()
            
            while time.time() - start_time < self.timeout:
                # Refresh to get updated status
                task.refresh()
                
                if task.status == "completed":
                    # Update task history
                    task_info['status'] = 'completed'
                    task_info['timestamp'] = time.time()
                    logger.info(f"Task {task_id} completed successfully")
                    return task.result
                
                if task.status == "failed":
                    # Update task history
                    task_info['status'] = 'failed'
                    task_info['timestamp'] = time.time()
                    error_msg = f"Task {task_id} failed with status: {task.status}"
                    logger.error(error_msg)
                    return {"status": "failed", "message": error_msg}
                
                # Sleep for a short time before checking again
                time.sleep(2)
            
            # If we get here, the task timed out
            task_info['status'] = 'timeout'
            task_info['timestamp'] = time.time()
            error_msg = f"Task {task_id} timed out after {self.timeout} seconds"
            logger.error(error_msg)
            return {"status": "timeout", "message": error_msg}
            
        except Exception as e:
            logger.error(f"Error executing custom template: {e}")
            return {"status": "error", "message": str(e)}

# Example usage
if __name__ == "__main__":
    # Create an instance of CodegenMCPCallable
    mcp = CodegenMCPCallable()
    
    # Example: Create a PR
    result = mcp.create_pr(
        context="Create a pull request for adding user authentication features. The changes include new login/logout endpoints, JWT token handling, and user session management."
    )
    
    print(f"Result: {result}")

