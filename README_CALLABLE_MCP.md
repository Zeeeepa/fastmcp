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

## Environment Variables

The following environment variables can be set:

- `ORG_ID`: Your organization ID (default: "323")
- `API_TOKEN`: Your API token (default: "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

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

## License

MIT
