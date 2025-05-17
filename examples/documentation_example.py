"""
Example of using the documentation creation endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Run on task
task_result = mcp.create_documentation(
    context="Create comprehensive documentation for a REST API that provides user authentication, product management, and order processing functionality. Include endpoints, request/response formats, authentication requirements, and example usage."
)

# Print the result
print(task_result)

