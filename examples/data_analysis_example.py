"""
Example of using the data analysis endpoint.
"""

from codegen_mcp_callable import CodegenMCPCallable

# Create an instance of CodegenMCPCallable
mcp = CodegenMCPCallable(org_id="323", token="sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99")

# Define the data analysis context
context = """
Analyze the following sales data and provide insights on trends, patterns, and recommendations for improving sales performance:

Monthly Sales Data (2023):
January: $120,000
February: $115,000
March: $150,000
April: $145,000
May: $160,000
June: $175,000
July: $190,000
August: $200,000
September: $180,000
October: $195,000
November: $210,000
December: $230,000

Product Category Sales:
Electronics: 35%
Clothing: 25%
Home Goods: 20%
Beauty: 15%
Other: 5%

Regional Sales:
North: $650,000
South: $580,000
East: $720,000
West: $545,000

Customer Segments:
New Customers: 30%
Returning Customers: 45%
Loyal Customers (>5 purchases): 25%
"""

# Run on task
task_result = mcp.analyze_data(context=context)

# Print the result
print(task_result)
