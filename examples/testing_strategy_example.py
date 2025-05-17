"""
Example of using the testing strategy creation endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Define the testing strategy creation context
context = """
Develop a comprehensive testing strategy for an e-commerce platform with the following components:

1. User Authentication System
   - Registration
   - Login/Logout
   - Password Reset
   - Profile Management

2. Product Catalog
   - Product Listing
   - Product Search
   - Product Filtering
   - Product Details

3. Shopping Cart
   - Add/Remove Items
   - Update Quantities
   - Apply Coupons
   - Calculate Totals

4. Checkout Process
   - Shipping Information
   - Payment Processing
   - Order Confirmation
   - Email Notifications

5. Order Management
   - Order History
   - Order Tracking
   - Order Cancellation
   - Returns/Refunds

The platform is built with a microservices architecture using:
- Frontend: React.js
- Backend: Node.js with Express
- Database: MongoDB
- Payment Gateway: Stripe
- Email Service: SendGrid

The testing strategy should cover:
- Unit Testing
- Integration Testing
- End-to-End Testing
- Performance Testing
- Security Testing
- Accessibility Testing
- Mobile Responsiveness Testing
"""

# Run on task
task_result = mcp.create_testing_strategy(context=context)

# Print the result
print(task_result)
