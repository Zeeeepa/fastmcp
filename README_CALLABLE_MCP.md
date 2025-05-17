# Codegen MCP Callable Server

A Python callable server that provides 6 specialized endpoints for interacting with the Codegen Agent API.

## Overview

This implementation provides a simple, callable interface for leveraging the Codegen Agent API with specialized prompt templates for different use cases. It exposes 6 methods that format inputs according to specialized templates before executing them through the Codegen Agent.

## Available Endpoints

1. **PR Creation**: Generate GitHub PR descriptions and metadata
2. **Linear Issues**: Create structured main issues and sub-issues for Linear
3. **Code Generation**: Generate optimized code implementations
4. **Data Analysis**: Analyze data and provide insights
5. **Documentation**: Create comprehensive documentation
6. **Testing Strategy**: Develop testing approaches and test cases

## Installation

```bash
# Clone the repository
git clone https://github.com/Zeeeepa/fastmcp.git
cd fastmcp

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Execute PR creation
result = mcp.create_pr(
    context="Create a pull request for adding user authentication features."
)

# Print the result
print(result)
```

### Available Methods

The `CodegenMCPCallable` class provides the following methods:

1. `create_pr(context, additional_params=None)`: Generate PR descriptions and metadata
2. `create_linear_issues(context, additional_params=None)`: Create structured main and sub-issues for Linear
3. `generate_code(context, additional_params=None)`: Generate optimized code implementations
4. `analyze_data(context, additional_params=None)`: Analyze data and provide insights
5. `create_documentation(context, additional_params=None)`: Create comprehensive documentation
6. `create_testing_strategy(context, additional_params=None)`: Develop testing approaches and test cases

Each method takes a `context` parameter (the input query or context text) and an optional `additional_params` dictionary for any additional parameters.

### Working with Templates

The `CodegenMCPCallable` class also provides methods for working with templates:

1. `get_template(template_key)`: Get the template for a specific key
2. `set_template(template_key, template)`: Set or update a template
3. `add_template(template_key, template)`: Add a new template
4. `delete_template(template_key)`: Delete a template
5. `list_templates()`: List all available templates

Example of customizing a template:

```python
from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable()

# Get the PR creation template
pr_template = mcp.get_template("pr_creation")
print(f"Original template: {pr_template}")

# Customize the PR creation template
custom_pr_template = """[CUSTOM PR CREATION TEMPLATE]
You are tasked with creating a detailed GitHub Pull Request for the following changes.

Custom instructions for PR creation:
- Create a descriptive title with the format: [FEATURE/FIX/REFACTOR] Brief description
- Write a comprehensive description with sections: Summary, Changes, Testing, Screenshots
- Include links to related issues using the format #issue_number
- List all files modified with brief explanations
- Add notes about any configuration changes required
- Suggest specific reviewers based on the code areas modified

Please analyze the following context and create a comprehensive PR:

{context}
"""

# Set the custom template
mcp.set_template("pr_creation", custom_pr_template)

# Use the custom template
result = mcp.create_pr(
    context="Create a pull request for adding user authentication features."
)

print(result)
```

Available template keys:
- `pr_creation`: Template for PR creation
- `linear_issues`: Template for Linear issues creation
- `code_generation`: Template for code generation
- `data_analysis`: Template for data analysis
- `documentation`: Template for documentation creation
- `testing_strategy`: Template for testing strategy creation

### Advanced Features

The `CodegenMCPCallable` class also provides advanced features:

1. `execute_custom_template(template, context, additional_params=None)`: Execute a custom template without adding it to the templates dictionary
2. `get_task_history()`: Get the history of executed tasks
3. `clear_task_history()`: Clear the task history

Example of using advanced features:

```python
from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable with custom timeout
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99", timeout=600)

# Add a new custom template
custom_template = """[CUSTOM API DOCUMENTATION TEMPLATE]
You are tasked with creating API documentation based on the following details.

Instructions for API documentation:
- Document each endpoint with its URL, method, request parameters, and response format
- Include authentication requirements
- Provide example requests and responses
- Document error codes and their meanings
- Include rate limiting information

Please analyze the following context and create comprehensive API documentation:

{context}
"""

# Add the custom template
mcp.add_template("api_documentation", custom_template)

# Use the custom template
result = mcp._execute_template("api_documentation", context)

# Execute a one-time custom template
one_time_template = """[ONE-TIME TEMPLATE]
You are tasked with creating a project roadmap based on the following details.

Instructions for roadmap creation:
- Identify key milestones and deliverables
- Estimate timelines for each milestone
- Identify dependencies between milestones
- Suggest resource allocation

Please analyze the following context and create a comprehensive project roadmap:

{context}
"""

result = mcp.execute_custom_template(one_time_template, context)

# Get task history
task_history = mcp.get_task_history()
print(f"Task history: {task_history}")

# Clear task history
mcp.clear_task_history()
```

## Environment Variables

The following environment variables can be set:

- `ORG_ID`: Your organization ID (default: "323")
- `API_TOKEN`: Your API token (default: "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")
- `DEFAULT_TIMEOUT`: Default timeout in seconds for agent tasks (default: 300)

You can set these in a `.env` file or pass them directly to the `CodegenMCPCallable` constructor.

## Dependencies

This implementation requires the following dependencies:

- `codegen`: The Codegen Python SDK
- `python-dotenv`: For loading environment variables
- Other dependencies as specified in `requirements.txt`

## Examples

See the `examples` directory for example usage of each endpoint:

- `examples/pr_creation_example.py`: Example of using the PR creation endpoint
- `examples/linear_issues_example.py`: Example of using the Linear issues creation endpoint
- `examples/code_generation_example.py`: Example of using the code generation endpoint
- `examples/data_analysis_example.py`: Example of using the data analysis endpoint
- `examples/documentation_example.py`: Example of using the documentation creation endpoint
- `examples/testing_strategy_example.py`: Example of using the testing strategy creation endpoint
- `examples/template_usage_example.py`: Example of customizing and using templates
- `examples/advanced_features_example.py`: Example of using advanced features

## Error Handling

The implementation includes comprehensive error handling:

- Logging of all operations and errors
- Timeout handling for agent tasks
- Validation of template keys
- Protection of default templates from deletion
- Detailed error messages for all operations

## License

MIT

