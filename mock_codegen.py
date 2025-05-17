"""
Mock implementation of the Codegen SDK for testing purposes.
"""

import time
import random
from typing import Dict, Any, Optional, List, Union


class Task:
    """
    Mock implementation of a Codegen Task.
    """
    
    def __init__(self, prompt: str):
        """
        Initialize a mock Task.
        
        Args:
            prompt: The prompt text
        """
        self.prompt = prompt
        self.status = "pending"
        self.result = None
        self._start_time = time.time()
    
    def refresh(self) -> None:
        """
        Simulate refreshing the task status.
        """
        # Simulate task completion after a short delay
        elapsed = time.time() - self._start_time
        
        if elapsed < 1.0:
            self.status = "running"
        else:
            self.status = "completed"
            self._generate_mock_result()
    
    def _generate_mock_result(self) -> None:
        """
        Generate a mock result based on the prompt.
        """
        # Extract the template type from the prompt
        template_type = None
        if "[PR CREATION TEMPLATE]" in self.prompt:
            template_type = "pr_creation"
        elif "[LINEAR ISSUE CREATION TEMPLATE]" in self.prompt:
            template_type = "linear_issues"
        elif "[CODE GENERATION TEMPLATE]" in self.prompt:
            template_type = "code_generation"
        elif "[DATA ANALYSIS TEMPLATE]" in self.prompt:
            template_type = "data_analysis"
        elif "[DOCUMENTATION TEMPLATE]" in self.prompt:
            template_type = "documentation"
        elif "[TESTING STRATEGY TEMPLATE]" in self.prompt:
            template_type = "testing_strategy"
        
        # Generate a mock result based on the template type
        if template_type == "pr_creation":
            self.result = self._mock_pr_creation_result()
        elif template_type == "linear_issues":
            self.result = self._mock_linear_issues_result()
        elif template_type == "code_generation":
            self.result = self._mock_code_generation_result()
        elif template_type == "data_analysis":
            self.result = self._mock_data_analysis_result()
        elif template_type == "documentation":
            self.result = self._mock_documentation_result()
        elif template_type == "testing_strategy":
            self.result = self._mock_testing_strategy_result()
        else:
            self.result = {"message": "Mock result for unknown template type"}
    
    def _mock_pr_creation_result(self) -> Dict[str, Any]:
        """
        Generate a mock PR creation result.
        """
        return {
            "title": "Add User Authentication Features",
            "description": "This PR adds user authentication features including login/logout endpoints, JWT token handling, and user session management.",
            "files_modified": [
                "auth/login.py",
                "auth/logout.py",
                "auth/jwt.py",
                "auth/session.py"
            ],
            "breaking_changes": False,
            "reviewers": ["@john", "@jane"]
        }
    
    def _mock_linear_issues_result(self) -> Dict[str, Any]:
        """
        Generate a mock Linear issues result.
        """
        return {
            "main_issue": {
                "title": "Implement User Authentication System",
                "description": "Create a comprehensive user authentication system with registration, login, password reset, and profile management features.",
                "priority": "high",
                "estimate": "2 weeks"
            },
            "sub_issues": [
                {
                    "title": "Implement User Registration API",
                    "description": "Create an API endpoint for user registration with email verification.",
                    "priority": "high",
                    "estimate": "3 days",
                    "acceptance_criteria": [
                        "Validate email format",
                        "Check for existing users",
                        "Send verification email",
                        "Store user data securely"
                    ]
                },
                {
                    "title": "Implement Login API",
                    "description": "Create an API endpoint for user login with JWT token generation.",
                    "priority": "high",
                    "estimate": "2 days",
                    "acceptance_criteria": [
                        "Validate credentials",
                        "Generate JWT token",
                        "Return appropriate error messages",
                        "Log login attempts"
                    ]
                },
                {
                    "title": "Implement Password Reset API",
                    "description": "Create an API endpoint for password reset with email verification.",
                    "priority": "medium",
                    "estimate": "2 days",
                    "acceptance_criteria": [
                        "Send reset email",
                        "Validate reset token",
                        "Update password securely",
                        "Invalidate old tokens"
                    ]
                },
                {
                    "title": "Implement Profile Management API",
                    "description": "Create an API endpoint for user profile management.",
                    "priority": "medium",
                    "estimate": "3 days",
                    "acceptance_criteria": [
                        "Update user profile data",
                        "Upload profile picture",
                        "Change email with verification",
                        "Delete account option"
                    ]
                }
            ]
        }
    
    def _mock_code_generation_result(self) -> Dict[str, Any]:
        """
        Generate a mock code generation result.
        """
        return {
            "code": """
def sum_even_numbers(numbers):
    \"\"\"
    Calculate the sum of all even numbers in the list.
    
    Args:
        numbers: A list of integers
        
    Returns:
        The sum of all even numbers in the list
        
    Raises:
        TypeError: If the input is not a list or contains non-integer values
    \"\"\"
    # Check if input is a list
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    # Handle empty list
    if not numbers:
        return 0
    
    # Calculate sum of even numbers
    total = 0
    for num in numbers:
        # Check if item is an integer
        if not isinstance(num, int):
            raise TypeError(f"All items must be integers, found {type(num).__name__}")
        
        # Add to total if even
        if num % 2 == 0:
            total += num
    
    return total
""",
            "language": "python",
            "explanation": "This function takes a list of integers and returns the sum of all even numbers. It includes error handling for invalid inputs and handles the edge case of an empty list.",
            "usage_example": """
# Example usage
numbers = [1, 2, 3, 4, 5, 6]
result = sum_even_numbers(numbers)  # Returns 12 (2 + 4 + 6)

# Edge cases
empty_list = []
result = sum_even_numbers(empty_list)  # Returns 0

# Error cases
try:
    result = sum_even_numbers("not a list")  # Raises TypeError
except TypeError as e:
    print(e)  # "Input must be a list"

try:
    result = sum_even_numbers([1, 2, "3"])  # Raises TypeError
except TypeError as e:
    print(e)  # "All items must be integers, found str"
"""
        }
    
    def _mock_data_analysis_result(self) -> Dict[str, Any]:
        """
        Generate a mock data analysis result.
        """
        return {
            "summary": "Analysis of sales data for Q1-Q3 2023",
            "key_findings": [
                "Overall sales increased by 15% compared to the same period last year",
                "Product category A showed the highest growth at 28%",
                "Region X underperformed with a 5% decrease in sales",
                "Customer segment Y contributed 40% of total revenue"
            ],
            "trends": [
                "Seasonal pattern with peaks in March and August",
                "Increasing adoption of premium products",
                "Shift from in-store to online purchases"
            ],
            "recommendations": [
                "Increase marketing budget for product category A",
                "Develop targeted promotions for region X",
                "Expand premium product offerings",
                "Optimize online shopping experience"
            ],
            "visualizations": [
                "Monthly sales trend chart",
                "Product category comparison",
                "Regional performance heatmap",
                "Customer segment distribution"
            ]
        }
    
    def _mock_documentation_result(self) -> Dict[str, Any]:
        """
        Generate a mock documentation result.
        """
        return {
            "title": "User Authentication API Documentation",
            "overview": "This API provides endpoints for user authentication, product management, and order processing.",
            "authentication": {
                "method": "JWT Bearer Token",
                "endpoint": "/api/auth/login",
                "example": "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            },
            "endpoints": [
                {
                    "path": "/api/auth/register",
                    "method": "POST",
                    "description": "Register a new user",
                    "request_body": {
                        "email": "string",
                        "password": "string",
                        "name": "string"
                    },
                    "response": {
                        "user_id": "string",
                        "email": "string",
                        "name": "string",
                        "created_at": "string (ISO date)"
                    },
                    "status_codes": [
                        "201: Created",
                        "400: Bad Request",
                        "409: Conflict (Email already exists)"
                    ]
                },
                {
                    "path": "/api/auth/login",
                    "method": "POST",
                    "description": "Authenticate a user and get a token",
                    "request_body": {
                        "email": "string",
                        "password": "string"
                    },
                    "response": {
                        "token": "string",
                        "user": {
                            "user_id": "string",
                            "email": "string",
                            "name": "string"
                        }
                    },
                    "status_codes": [
                        "200: OK",
                        "400: Bad Request",
                        "401: Unauthorized"
                    ]
                }
            ],
            "example_usage": {
                "curl": "curl -X POST https://api.example.com/api/auth/login -H 'Content-Type: application/json' -d '{\"email\":\"user@example.com\",\"password\":\"password123\"}'",
                "python": "import requests\n\nresponse = requests.post('https://api.example.com/api/auth/login', json={'email': 'user@example.com', 'password': 'password123'})\ntoken = response.json()['token']",
                "javascript": "fetch('https://api.example.com/api/auth/login', {\n  method: 'POST',\n  headers: { 'Content-Type': 'application/json' },\n  body: JSON.stringify({ email: 'user@example.com', password: 'password123' })\n})\n.then(response => response.json())\n.then(data => {\n  const token = data.token;\n});"
            }
        }
    
    def _mock_testing_strategy_result(self) -> Dict[str, Any]:
        """
        Generate a mock testing strategy result.
        """
        return {
            "overview": "Comprehensive testing strategy for an e-commerce platform with microservices architecture",
            "testing_levels": [
                {
                    "level": "Unit Testing",
                    "description": "Testing individual components in isolation",
                    "tools": ["pytest", "Jest"],
                    "coverage_target": "90%",
                    "key_areas": [
                        "Authentication logic",
                        "Product validation",
                        "Order calculations",
                        "Form validation"
                    ]
                },
                {
                    "level": "Integration Testing",
                    "description": "Testing interactions between components",
                    "tools": ["pytest", "Supertest"],
                    "coverage_target": "80%",
                    "key_areas": [
                        "API endpoints",
                        "Database interactions",
                        "Service communications",
                        "External service integrations"
                    ]
                },
                {
                    "level": "End-to-End Testing",
                    "description": "Testing complete user flows",
                    "tools": ["Cypress", "Selenium"],
                    "coverage_target": "70%",
                    "key_areas": [
                        "User registration and login",
                        "Product browsing and search",
                        "Shopping cart operations",
                        "Checkout process",
                        "Order management"
                    ]
                }
            ],
            "performance_testing": {
                "tools": ["k6", "JMeter"],
                "scenarios": [
                    "Load testing with 1000 concurrent users",
                    "Stress testing to identify breaking points",
                    "Endurance testing for 24-hour stability"
                ],
                "key_metrics": [
                    "Response time < 200ms for API calls",
                    "Throughput > 500 requests/second",
                    "Error rate < 0.1%"
                ]
            },
            "security_testing": {
                "tools": ["OWASP ZAP", "SonarQube"],
                "focus_areas": [
                    "Authentication and authorization",
                    "Input validation",
                    "Data encryption",
                    "Session management",
                    "API security"
                ]
            },
            "test_environments": [
                {
                    "name": "Development",
                    "purpose": "For developers to run tests locally",
                    "configuration": "Docker containers with mocked external services"
                },
                {
                    "name": "CI/CD",
                    "purpose": "Automated testing in the pipeline",
                    "configuration": "Ephemeral environments with test databases"
                },
                {
                    "name": "Staging",
                    "purpose": "Pre-production validation",
                    "configuration": "Mirror of production with sanitized data"
                }
            ],
            "test_data_strategy": {
                "approach": "Combination of generated and fixed test data",
                "tools": ["Faker", "Factory Boy"],
                "considerations": [
                    "Data privacy compliance",
                    "Realistic data scenarios",
                    "Edge cases coverage"
                ]
            }
        }


class Agent:
    """
    Mock implementation of a Codegen Agent.
    """
    
    def __init__(self, org_id: str, token: str):
        """
        Initialize a mock Agent.
        
        Args:
            org_id: The organization ID
            token: The API token
        """
        self.org_id = org_id
        self.token = token
    
    def run(self, prompt: str) -> Task:
        """
        Run a task with the given prompt.
        
        Args:
            prompt: The prompt text
            
        Returns:
            A Task object
        """
        return Task(prompt)

