"""
Example of using the PR creation endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Define the PR creation context
context = """
Create a pull request for adding user authentication features. 
The changes include new login/logout endpoints, JWT token handling, and user session management.
"""

# Optional: Get and print the template being used
pr_template = mcp.get_template("pr_creation")
print("PR Creation Template:")
print(pr_template)
print("\n" + "-" * 80 + "\n")

# Run on task
task_result = mcp.create_pr(context=context)

# Print the result
print("PR Creation Result:")
print(task_result)

