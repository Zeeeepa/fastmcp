"""
Example of using the Linear issues creation endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Run on task
task_result = mcp.create_linear_issues(
    context="Create a main issue and sub-issues for implementing a user authentication system. The system should include registration, login, password reset, and profile management features. Each feature should be implemented as a separate API endpoint with appropriate validation and error handling."
)

# Print the result
print(task_result)

