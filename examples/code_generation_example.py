"""
Example of using the code generation endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Define the code generation context
context = """
Create a Python function that takes a list of integers and returns the sum of all even numbers in the list. 
The function should handle edge cases like empty lists and non-integer inputs.
"""

# Run on task
task_result = mcp.generate_code(context=context)

# Print the result
print(task_result)
