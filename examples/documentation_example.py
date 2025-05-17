"""
Example of using the documentation creation endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Define the documentation creation context
context = """
Create comprehensive documentation for a RESTful API that provides user authentication and product management functionality.

The API includes the following endpoints:
1. POST /api/auth/register - Register a new user
2. POST /api/auth/login - Authenticate a user and get a token
3. GET /api/auth/profile - Get the authenticated user's profile
4. PUT /api/auth/profile - Update the authenticated user's profile
5. POST /api/auth/logout - Logout a user
6. POST /api/auth/reset-password - Request a password reset
7. POST /api/auth/reset-password/:token - Reset a password with a token
8. GET /api/products - Get a list of products
9. GET /api/products/:id - Get a product by ID
10. POST /api/products - Create a new product (admin only)
11. PUT /api/products/:id - Update a product (admin only)
12. DELETE /api/products/:id - Delete a product (admin only)

The documentation should include:
- Overview of the API
- Authentication methods
- Endpoint descriptions
- Request/response formats
- Status codes
- Error handling
- Example usage with curl, Python, and JavaScript
"""

# Run on task
task_result = mcp.create_documentation(context=context)

# Print the result
print(task_result)
