"""
Example of using the data analysis endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Run on task
task_result = mcp.analyze_data(
    context="Analyze the following sales data and provide insights on trends, patterns, and recommendations for improving sales performance: [Sales data would be provided here]"
)

# Print the result
print(task_result)

