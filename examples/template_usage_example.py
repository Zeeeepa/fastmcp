"""
Example of using and customizing templates.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Get the PR creation template
pr_template = mcp.get_template("pr_creation")
print("Original PR Creation Template:")
print(pr_template)
print("\n" + "-" * 80 + "\n")

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

# Get the updated template
updated_pr_template = mcp.get_template("pr_creation")
print("Updated PR Creation Template:")
print(updated_pr_template)
print("\n" + "-" * 80 + "\n")

# Use the custom template
context = """
Create a pull request for implementing a new user authentication system.
The system includes:
- User registration with email verification
- Login with JWT token generation
- Password reset functionality
- User profile management
- Role-based access control
- Session management with refresh tokens
- OAuth integration with Google and GitHub
"""

# Run on task with the custom template
task_result = mcp.create_pr(context=context)

# Print the result
print("PR Creation Result:")
print(task_result)

# Reset to the original template (for demonstration purposes)
mcp.set_template("pr_creation", pr_template)

