FROM python:3.9-slim

# Create a non-root user
RUN groupadd -r codegen && useradd -r -g codegen codegen

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install codegen

# Copy the application code
COPY . .

# Set ownership
RUN chown -R codegen:codegen /app

# Switch to non-root user
USER codegen

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CODEGEN_ORG_ID=""
ENV CODEGEN_TOKEN=""
ENV MCP_HOST="0.0.0.0"
ENV MCP_PORT="8000"
ENV LOG_LEVEL="INFO"

# Expose the port
EXPOSE 8000

# Run the server
CMD ["python", "examples/codegen_agent_server.py"]

