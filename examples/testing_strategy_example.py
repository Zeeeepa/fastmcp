"""
Example of using the testing strategy creation endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Run on task
task_result = mcp.create_testing_strategy(
    context="Develop a comprehensive testing strategy for a new e-commerce platform that includes user authentication, product browsing, shopping cart, checkout, and order management features. The platform is built using a microservices architecture with Python FastAPI backends and a React frontend."
)

# Print the result
print(task_result)

