"""
Codegen Agent MCP Server.

This module provides a FastMCP server that integrates with the Codegen Agent API,
offering 6 callable endpoints for different operations.
"""

import asyncio
from typing import Dict, Any, Optional, List

from fastmcp import FastMCP, Context
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent

from .agent import Agent, CodegenTask


class CodegenAgentServer(FastMCP):
    """
    FastMCP server for the Codegen Agent API.
    
    This server provides 6 callable endpoints for different Codegen Agent operations,
    each using a specific prompt template.
    """
    
    def __init__(
        self,
        org_id: str,
        api_token: str,
        name: str = "Codegen Agent",
        host: str = "127.0.0.1",
        port: int = 8000,
        **kwargs
    ):
        """
        Initialize the Codegen Agent MCP Server.
        
        Args:
            org_id: Organization ID for authentication
            api_token: API token for authentication
            name: Name of the server
            host: Host address for HTTP transport
            port: Port number for HTTP transport
            **kwargs: Additional arguments to pass to FastMCP
        """
        super().__init__(
            name=name,
            host=host,
            port=port,
            instructions="""
            This server provides access to the Codegen Agent API through 6 callable endpoints:
            
            1. code_generation - Generate code based on a description
            2. code_explanation - Explain existing code
            3. code_refactoring - Refactor code based on requirements
            4. bug_fixing - Fix bugs in code
            5. code_review - Review code and provide feedback
            6. documentation - Generate documentation for code
            
            Each endpoint accepts specific parameters and returns the result from the Codegen Agent.
            """,
            **kwargs
        )
        
        # Initialize the Codegen Agent
        self.agent = Agent(org_id, api_token)
        
        # Register prompts
        self._register_prompts()
        
        # Register resources
        self._register_resources()
    
    def _register_prompts(self):
        """Register all prompt templates for the Codegen Agent."""
        
        @self.prompt(name="code_generation")
        def code_generation_prompt(
            description: str,
            language: str,
            additional_context: Optional[str] = None
        ) -> str:
            """
            Generate code based on a description.
            
            Args:
                description: Description of the code to generate
                language: Programming language to use
                additional_context: Additional context or requirements
                
            Returns:
                A prompt for code generation
            """
            prompt = f"Generate {language} code that accomplishes the following: {description}"
            
            if additional_context:
                prompt += f"\n\nAdditional context: {additional_context}"
                
            return prompt
        
        @self.prompt(name="code_explanation")
        def code_explanation_prompt(
            code: str,
            detail_level: str = "medium"
        ) -> str:
            """
            Explain existing code.
            
            Args:
                code: The code to explain
                detail_level: Level of detail for the explanation (low, medium, high)
                
            Returns:
                A prompt for code explanation
            """
            return f"""
            Please explain the following code with a {detail_level} level of detail:
            
            ```
            {code}
            ```
            """
        
        @self.prompt(name="code_refactoring")
        def code_refactoring_prompt(
            code: str,
            requirements: str,
            preserve_functionality: bool = True
        ) -> str:
            """
            Refactor code based on requirements.
            
            Args:
                code: The code to refactor
                requirements: Requirements for the refactoring
                preserve_functionality: Whether to preserve the original functionality
                
            Returns:
                A prompt for code refactoring
            """
            preserve_text = "while preserving the original functionality" if preserve_functionality else ""
            
            return f"""
            Please refactor the following code {preserve_text} according to these requirements:
            
            Requirements: {requirements}
            
            ```
            {code}
            ```
            """
        
        @self.prompt(name="bug_fixing")
        def bug_fixing_prompt(
            code: str,
            bug_description: str,
            expected_behavior: Optional[str] = None
        ) -> str:
            """
            Fix bugs in code.
            
            Args:
                code: The code containing bugs
                bug_description: Description of the bug
                expected_behavior: Description of the expected behavior
                
            Returns:
                A prompt for bug fixing
            """
            prompt = f"""
            Please fix the following code that has a bug:
            
            Bug description: {bug_description}
            
            ```
            {code}
            ```
            """
            
            if expected_behavior:
                prompt += f"\n\nExpected behavior: {expected_behavior}"
                
            return prompt
        
        @self.prompt(name="code_review")
        def code_review_prompt(
            code: str,
            focus_areas: Optional[List[str]] = None,
            standards: Optional[str] = None
        ) -> str:
            """
            Review code and provide feedback.
            
            Args:
                code: The code to review
                focus_areas: Specific areas to focus on during the review
                standards: Coding standards to apply
                
            Returns:
                A prompt for code review
            """
            prompt = "Please review the following code"
            
            if standards:
                prompt += f" according to {standards} standards"
                
            if focus_areas:
                areas = ", ".join(focus_areas)
                prompt += f", focusing on: {areas}"
                
            prompt += f":\n\n```\n{code}\n```"
            
            return prompt
        
        @self.prompt(name="documentation")
        def documentation_prompt(
            code: str,
            doc_format: str = "markdown",
            include_examples: bool = True
        ) -> str:
            """
            Generate documentation for code.
            
            Args:
                code: The code to document
                doc_format: Format for the documentation (markdown, rst, html)
                include_examples: Whether to include examples in the documentation
                
            Returns:
                A prompt for documentation generation
            """
            examples_text = "including usage examples" if include_examples else ""
            
            return f"""
            Please generate {doc_format} documentation {examples_text} for the following code:
            
            ```
            {code}
            ```
            """
    
    def _register_resources(self):
        """Register resources for accessing prompt templates."""
        
        @self.resource("codegen://prompts")
        def get_prompt_templates() -> Dict[str, str]:
            """
            Get all available prompt templates.
            
            Returns:
                A dictionary of prompt templates with their descriptions
            """
            return {
                "code_generation": "Generate code based on a description",
                "code_explanation": "Explain existing code",
                "code_refactoring": "Refactor code based on requirements",
                "bug_fixing": "Fix bugs in code",
                "code_review": "Review code and provide feedback",
                "documentation": "Generate documentation for code"
            }
        
        @self.resource("codegen://prompts/{prompt_name}")
        def get_prompt_template(prompt_name: str) -> Dict[str, Any]:
            """
            Get a specific prompt template.
            
            Args:
                prompt_name: Name of the prompt template
                
            Returns:
                Details about the prompt template
            """
            prompts = {
                "code_generation": {
                    "description": "Generate code based on a description",
                    "parameters": {
                        "description": "Description of the code to generate",
                        "language": "Programming language to use",
                        "additional_context": "Additional context or requirements (optional)"
                    }
                },
                "code_explanation": {
                    "description": "Explain existing code",
                    "parameters": {
                        "code": "The code to explain",
                        "detail_level": "Level of detail for the explanation (low, medium, high)"
                    }
                },
                "code_refactoring": {
                    "description": "Refactor code based on requirements",
                    "parameters": {
                        "code": "The code to refactor",
                        "requirements": "Requirements for the refactoring",
                        "preserve_functionality": "Whether to preserve the original functionality"
                    }
                },
                "bug_fixing": {
                    "description": "Fix bugs in code",
                    "parameters": {
                        "code": "The code containing bugs",
                        "bug_description": "Description of the bug",
                        "expected_behavior": "Description of the expected behavior (optional)"
                    }
                },
                "code_review": {
                    "description": "Review code and provide feedback",
                    "parameters": {
                        "code": "The code to review",
                        "focus_areas": "Specific areas to focus on during the review (optional)",
                        "standards": "Coding standards to apply (optional)"
                    }
                },
                "documentation": {
                    "description": "Generate documentation for code",
                    "parameters": {
                        "code": "The code to document",
                        "doc_format": "Format for the documentation (markdown, rst, html)",
                        "include_examples": "Whether to include examples in the documentation"
                    }
                }
            }
            
            if prompt_name not in prompts:
                return {"error": f"Prompt template '{prompt_name}' not found"}
                
            return prompts[prompt_name]
    
    @staticmethod
    async def run_codegen_agent(prompt: str, ctx: Context) -> Dict[str, Any]:
        """
        Run the Codegen Agent with the given prompt.
        
        This is the core function that executes the Codegen Agent with a prompt
        and returns the result.
        
        Args:
            prompt: The prompt to send to the Codegen Agent
            ctx: The MCP context
            
        Returns:
            The result from the Codegen Agent
        """
        # Get the agent instance from the server
        agent = ctx.server.agent
        
        # Run the agent with the prompt
        task = await agent.run(prompt)
        
        # Wait for the task to complete
        while task.status in ["pending", "running"]:
            await asyncio.sleep(0.5)
            task.refresh()
        
        # Return the result
        if task.status == "completed":
            return {
                "status": "success",
                "task_id": task.task_id,
                "result": task.result
            }
        else:
            return {
                "status": "error",
                "task_id": task.task_id,
                "error": task.error or "Unknown error"
            }
    
    def configure_tools(self):
        """Configure tools for the Codegen Agent operations."""
        
        @self.tool()
        async def generate_code(
            description: str,
            language: str,
            additional_context: Optional[str] = None,
            ctx: Context = None
        ) -> Dict[str, Any]:
            """
            Generate code based on a description.
            
            Args:
                description: Description of the code to generate
                language: Programming language to use
                additional_context: Additional context or requirements
                ctx: The MCP context
                
            Returns:
                Generated code from the Codegen Agent
            """
            # Get the prompt from the prompt template
            prompt_template = ctx.server.prompts.get("code_generation")
            prompt = await prompt_template(description, language, additional_context)
            
            # Run the Codegen Agent
            return await self.run_codegen_agent(prompt, ctx)
        
        @self.tool()
        async def explain_code(
            code: str,
            detail_level: str = "medium",
            ctx: Context = None
        ) -> Dict[str, Any]:
            """
            Explain existing code.
            
            Args:
                code: The code to explain
                detail_level: Level of detail for the explanation (low, medium, high)
                ctx: The MCP context
                
            Returns:
                Explanation of the code from the Codegen Agent
            """
            # Get the prompt from the prompt template
            prompt_template = ctx.server.prompts.get("code_explanation")
            prompt = await prompt_template(code, detail_level)
            
            # Run the Codegen Agent
            return await self.run_codegen_agent(prompt, ctx)
        
        @self.tool()
        async def refactor_code(
            code: str,
            requirements: str,
            preserve_functionality: bool = True,
            ctx: Context = None
        ) -> Dict[str, Any]:
            """
            Refactor code based on requirements.
            
            Args:
                code: The code to refactor
                requirements: Requirements for the refactoring
                preserve_functionality: Whether to preserve the original functionality
                ctx: The MCP context
                
            Returns:
                Refactored code from the Codegen Agent
            """
            # Get the prompt from the prompt template
            prompt_template = ctx.server.prompts.get("code_refactoring")
            prompt = await prompt_template(code, requirements, preserve_functionality)
            
            # Run the Codegen Agent
            return await self.run_codegen_agent(prompt, ctx)
        
        @self.tool()
        async def fix_bug(
            code: str,
            bug_description: str,
            expected_behavior: Optional[str] = None,
            ctx: Context = None
        ) -> Dict[str, Any]:
            """
            Fix bugs in code.
            
            Args:
                code: The code containing bugs
                bug_description: Description of the bug
                expected_behavior: Description of the expected behavior
                ctx: The MCP context
                
            Returns:
                Fixed code from the Codegen Agent
            """
            # Get the prompt from the prompt template
            prompt_template = ctx.server.prompts.get("bug_fixing")
            prompt = await prompt_template(code, bug_description, expected_behavior)
            
            # Run the Codegen Agent
            return await self.run_codegen_agent(prompt, ctx)
        
        @self.tool()
        async def review_code(
            code: str,
            focus_areas: Optional[List[str]] = None,
            standards: Optional[str] = None,
            ctx: Context = None
        ) -> Dict[str, Any]:
            """
            Review code and provide feedback.
            
            Args:
                code: The code to review
                focus_areas: Specific areas to focus on during the review
                standards: Coding standards to apply
                ctx: The MCP context
                
            Returns:
                Code review feedback from the Codegen Agent
            """
            # Get the prompt from the prompt template
            prompt_template = ctx.server.prompts.get("code_review")
            prompt = await prompt_template(code, focus_areas, standards)
            
            # Run the Codegen Agent
            return await self.run_codegen_agent(prompt, ctx)
        
        @self.tool()
        async def generate_documentation(
            code: str,
            doc_format: str = "markdown",
            include_examples: bool = True,
            ctx: Context = None
        ) -> Dict[str, Any]:
            """
            Generate documentation for code.
            
            Args:
                code: The code to document
                doc_format: Format for the documentation (markdown, rst, html)
                include_examples: Whether to include examples in the documentation
                ctx: The MCP context
                
            Returns:
                Generated documentation from the Codegen Agent
            """
            # Get the prompt from the prompt template
            prompt_template = ctx.server.prompts.get("documentation")
            prompt = await prompt_template(code, doc_format, include_examples)
            
            # Run the Codegen Agent
            return await self.run_codegen_agent(prompt, ctx)

