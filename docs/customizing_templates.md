# Customizing Prompt Templates

This guide explains how to customize the prompt templates used by the Codegen Agent MCP Server.

## Understanding Prompt Templates

Prompt templates are pre-defined text patterns that guide the Codegen Agent's behavior for each endpoint. They include instructions and placeholders that are filled with user-provided values when the endpoint is called.

The default templates are defined in the `PROMPT_TEMPLATES` dictionary in the `codegen_agent_server.py` file.

## Default Templates

Here are the default templates for each endpoint:

### create_pr

```
Create a PR with the following specifications:

{agent_query}

Instructions:
- Create a new branch from the main branch
- Make the necessary changes
- Create a PR with a descriptive title and body
- Link any relevant issues
```

### create_linear_issues

```
Create a main issue and sub-issues in Linear with the following specifications:

{agent_query}

Instructions:
- Create a main issue with a descriptive title and body
- Create sub-issues for each discrete functionality
- Link the sub-issues to the main issue
- Assign appropriate labels and priorities
```

### analyze_codebase

```
Analyze the codebase and provide insights:

{agent_query}

Instructions:
- Analyze the structure of the codebase
- Identify potential issues or areas for improvement
- Provide recommendations for best practices
- Suggest optimizations if applicable
```

### fix_bug

```
Fix the bug in the codebase:

{agent_query}

Instructions:
- Identify the root cause of the bug
- Implement a fix
- Add tests to prevent regression
- Create a PR with the fix
```

### review_pr

```
Review the PR and provide feedback:

{agent_query}

Instructions:
- Review the code changes
- Check for potential issues or bugs
- Suggest improvements
- Provide constructive feedback
```

### generate_documentation

```
Generate documentation for the codebase:

{agent_query}

Instructions:
- Analyze the codebase structure
- Generate comprehensive documentation
- Include usage examples
- Explain key concepts and components
```

## Modifying Templates

To modify a template, edit the `PROMPT_TEMPLATES` dictionary in the `codegen_agent_server.py` file:

```python
PROMPT_TEMPLATES = {
    "create_pr": """
    Create a PR with the following specifications:
    
    {agent_query}
    
    Custom Instructions:
    - Create a new branch from the develop branch (not main)
    - Follow our company's coding standards
    - Include unit tests for all new functionality
    - Create a PR with a descriptive title and body
    - Link any relevant issues
    """,
    
    # Other templates...
}
```

## Template Placeholders

Each template can include the following placeholders:

- `{agent_query}`: The query provided by the user when calling the endpoint

## Adding New Templates

You can add new templates for custom endpoints:

1. Add a new template to the `PROMPT_TEMPLATES` dictionary:

```python
PROMPT_TEMPLATES = {
    # Existing templates...
    
    "custom_endpoint": """
    Custom endpoint instructions:
    
    {agent_query}
    
    Instructions:
    - Custom instruction 1
    - Custom instruction 2
    - Custom instruction 3
    """
}
```

2. Create a new endpoint function that uses the template:

```python
@mcp.tool()
async def custom_endpoint(
    agent_query: str, 
    ctx: Context,
    org_id: Optional[str] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Custom endpoint description.
    
    Args:
        agent_query: The query for the custom endpoint
        org_id: The organization ID (optional)
        token: The API token (optional)
        
    Returns:
        The result of the custom operation
    """
    return await run_codegen_agent(
        "custom_endpoint", 
        agent_query, 
        ctx,
        org_id or DEFAULT_ORG_ID,
        token or DEFAULT_TOKEN
    )
```

## Best Practices for Template Design

When designing prompt templates:

1. **Be Specific**: Provide clear, specific instructions to guide the agent's behavior.
2. **Include Context**: Give the agent enough context to understand the task.
3. **Define Expectations**: Clearly define what the output should look like.
4. **Use Consistent Formatting**: Maintain consistent formatting across templates.
5. **Test Thoroughly**: Test your templates with various inputs to ensure they produce the expected results.

## Accessing Templates Programmatically

You can access the templates programmatically using the provided resources:

```python
# Get all templates
templates = await client.read_resource("prompts://templates")
print(templates.content)

# Get a specific template
template = await client.read_resource("prompts://templates/create_pr")
print(template.content)
```

This allows you to inspect the templates before using them, which can be helpful for debugging or documentation purposes.

