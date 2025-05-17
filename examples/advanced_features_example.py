"""
Example of using the advanced features of CodegenMCPCallable.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable with custom timeout
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99", timeout=600)

print("=== Adding a Custom Template ===")
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

try:
    # Add the custom template
    mcp.add_template("api_documentation", custom_template)
    print("Custom template added successfully")
    
    # List all available templates
    templates = mcp.list_templates()
    print(f"Available templates: {list(templates.keys())}")
    
    # Use the custom template
    context = """
    Document a RESTful API for a task management system with the following endpoints:
    
    1. GET /api/tasks - Get all tasks
    2. GET /api/tasks/{id} - Get a task by ID
    3. POST /api/tasks - Create a new task
    4. PUT /api/tasks/{id} - Update a task
    5. DELETE /api/tasks/{id} - Delete a task
    
    The API requires JWT authentication with a token in the Authorization header.
    """
    
    print("\n=== Executing Custom Template ===")
    result = mcp._execute_template("api_documentation", context)
    print(f"Result snippet: {result[:200]}...")
    
    print("\n=== Using execute_custom_template Method ===")
    # Create another custom template without adding it to the templates dictionary
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
    
    context = """
    Create a roadmap for developing a mobile application with the following features:
    
    1. User authentication and profile management
    2. Task creation and management
    3. Calendar integration
    4. Push notifications
    5. Analytics dashboard
    
    The project has a team of 3 developers, 1 designer, and 1 product manager.
    The project should be completed within 6 months.
    """
    
    result = mcp.execute_custom_template(one_time_template, context)
    print(f"Result snippet: {result[:200]}...")
    
    print("\n=== Task History ===")
    # Get task history
    task_history = mcp.get_task_history()
    print(f"Task history: {task_history}")
    
    # Clear task history
    mcp.clear_task_history()
    print("Task history cleared")
    
    # Verify task history is empty
    task_history = mcp.get_task_history()
    print(f"Task history after clearing: {task_history}")
    
    print("\n=== Template Management ===")
    # Delete the custom template
    mcp.delete_template("api_documentation")
    print("Custom template deleted successfully")
    
    # Verify the template was deleted
    templates = mcp.list_templates()
    print(f"Available templates after deletion: {list(templates.keys())}")
    
except Exception as e:
    print(f"Error: {e}")

