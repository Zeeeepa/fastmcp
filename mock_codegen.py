"""
Mock implementation of the Codegen SDK for testing purposes.
"""

class Agent:
    def __init__(self, org_id=None, token=None):
        self.org_id = org_id
        self.token = token
    
    def run(self, prompt):
        """Run a task with the given prompt"""
        return Task(prompt)

class Task:
    def __init__(self, prompt):
        self.prompt = prompt
        self.status = "pending"
        self.result = None
    
    def refresh(self):
        """Simulate task completion"""
        self.status = "completed"
        self.result = f"Completed task with prompt: {self.prompt[:100]}..."

