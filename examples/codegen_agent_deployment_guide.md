# Codegen Agent MCP Server Deployment Guide

This guide provides comprehensive instructions for deploying the Codegen Agent MCP server in different environments. It covers local deployment, Docker deployment, cloud platform deployment, security considerations, and environment variable configuration.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Platform Deployment](#cloud-platform-deployment)
  - [AWS Deployment](#aws-deployment)
  - [Google Cloud Platform Deployment](#google-cloud-platform-deployment)
  - [Azure Deployment](#azure-deployment)
- [Security Considerations](#security-considerations)
- [Environment Variable Configuration](#environment-variable-configuration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying the Codegen Agent MCP server, ensure you have the following:

- Python 3.8 or higher
- pip (Python package manager)
- Codegen API credentials (organization ID and API token)
- Git (for cloning the repository)
- Docker (for containerized deployment)
- Access to a cloud platform (for cloud deployment)

## Local Deployment

Local deployment is ideal for development, testing, or small-scale usage. Follow these steps to deploy the Codegen Agent MCP server locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Zeeeepa/fastmcp.git
   cd fastmcp
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .  # Install the package in development mode
   pip install codegen  # Install the Codegen Agent library
   ```

4. **Configure environment variables**:
   ```bash
   export CODEGEN_ORG_ID="your-org-id"
   export CODEGEN_TOKEN="your-api-token"
   ```
   
   On Windows:
   ```cmd
   set CODEGEN_ORG_ID=your-org-id
   set CODEGEN_TOKEN=your-api-token
   ```

5. **Run the server**:
   ```bash
   python examples/codegen_agent_server.py
   ```

6. **Verify the deployment**:
   The server should start on `http://127.0.0.1:8000` by default. You can test it using the provided client example:
   ```bash
   python examples/codegen_agent_client.py
   ```

### Running as a Background Service

To run the server as a background service on Linux/macOS, you can use `nohup` or create a systemd service:

#### Using nohup:
```bash
nohup python examples/codegen_agent_server.py > codegen_mcp.log 2>&1 &
```

#### Using systemd:
1. Create a service file:
   ```bash
   sudo nano /etc/systemd/system/codegen-mcp.service
   ```

2. Add the following content:
   ```
   [Unit]
   Description=Codegen Agent MCP Server
   After=network.target

   [Service]
   User=your-username
   WorkingDirectory=/path/to/fastmcp
   Environment="CODEGEN_ORG_ID=your-org-id"
   Environment="CODEGEN_TOKEN=your-api-token"
   ExecStart=/path/to/python /path/to/fastmcp/examples/codegen_agent_server.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable codegen-mcp
   sudo systemctl start codegen-mcp
   ```

4. Check the status:
   ```bash
   sudo systemctl status codegen-mcp
   ```

## Docker Deployment

Docker deployment provides better isolation, portability, and scalability. Follow these steps to deploy the Codegen Agent MCP server using Docker:

1. **Create a Dockerfile**:
   Create a file named `Dockerfile` in the root directory of the project with the following content:

   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   # Copy the requirements and install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   RUN pip install codegen

   # Copy the application code
   COPY . .

   # Set environment variables
   ENV PYTHONUNBUFFERED=1
   ENV CODEGEN_ORG_ID=""
   ENV CODEGEN_TOKEN=""

   # Expose the port
   EXPOSE 8000

   # Run the server
   CMD ["python", "examples/codegen_agent_server.py"]
   ```

2. **Create a requirements.txt file**:
   ```
   fastmcp>=0.1.0
   ```

3. **Build the Docker image**:
   ```bash
   docker build -t codegen-mcp-server .
   ```

4. **Run the Docker container**:
   ```bash
   docker run -d \
     --name codegen-mcp \
     -p 8000:8000 \
     -e CODEGEN_ORG_ID=your-org-id \
     -e CODEGEN_TOKEN=your-api-token \
     codegen-mcp-server
   ```

5. **Verify the deployment**:
   The server should be accessible at `http://localhost:8000`. You can test it using curl or the client example.

### Using Docker Compose

For a more comprehensive setup, you can use Docker Compose:

1. **Create a docker-compose.yml file**:
   ```yaml
   version: '3'

   services:
     codegen-mcp:
       build: .
       ports:
         - "8000:8000"
       environment:
         - CODEGEN_ORG_ID=your-org-id
         - CODEGEN_TOKEN=your-api-token
       restart: unless-stopped
       volumes:
         - ./logs:/app/logs
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Stop the services**:
   ```bash
   docker-compose down
   ```

## Cloud Platform Deployment

Deploying to a cloud platform provides better scalability, reliability, and accessibility. Here are guides for deploying to major cloud platforms:

### AWS Deployment

#### Using AWS Elastic Beanstalk:

1. **Install the AWS CLI and EB CLI**:
   ```bash
   pip install awscli awsebcli
   ```

2. **Initialize EB application**:
   ```bash
   eb init -p python-3.8 codegen-mcp
   ```

3. **Create an EB environment**:
   ```bash
   eb create codegen-mcp-env
   ```

4. **Configure environment variables**:
   ```bash
   eb setenv CODEGEN_ORG_ID=your-org-id CODEGEN_TOKEN=your-api-token
   ```

5. **Deploy the application**:
   ```bash
   eb deploy
   ```

6. **Open the application**:
   ```bash
   eb open
   ```

#### Using AWS ECS (with Docker):

1. **Create an ECR repository**:
   ```bash
   aws ecr create-repository --repository-name codegen-mcp
   ```

2. **Authenticate Docker to ECR**:
   ```bash
   aws ecr get-login-password | docker login --username AWS --password-stdin your-account-id.dkr.ecr.region.amazonaws.com
   ```

3. **Tag and push the Docker image**:
   ```bash
   docker tag codegen-mcp-server your-account-id.dkr.ecr.region.amazonaws.com/codegen-mcp:latest
   docker push your-account-id.dkr.ecr.region.amazonaws.com/codegen-mcp:latest
   ```

4. **Create an ECS cluster, task definition, and service** using the AWS Management Console or AWS CLI.

### Google Cloud Platform Deployment

#### Using Google Cloud Run:

1. **Install the Google Cloud SDK**:
   Follow the instructions at https://cloud.google.com/sdk/docs/install

2. **Authenticate with GCP**:
   ```bash
   gcloud auth login
   ```

3. **Configure Docker to use GCP credentials**:
   ```bash
   gcloud auth configure-docker
   ```

4. **Tag and push the Docker image**:
   ```bash
   docker tag codegen-mcp-server gcr.io/your-project-id/codegen-mcp:latest
   docker push gcr.io/your-project-id/codegen-mcp:latest
   ```

5. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy codegen-mcp \
     --image gcr.io/your-project-id/codegen-mcp:latest \
     --platform managed \
     --set-env-vars CODEGEN_ORG_ID=your-org-id,CODEGEN_TOKEN=your-api-token
   ```

### Azure Deployment

#### Using Azure App Service:

1. **Install the Azure CLI**:
   Follow the instructions at https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

2. **Login to Azure**:
   ```bash
   az login
   ```

3. **Create a resource group**:
   ```bash
   az group create --name codegen-mcp-group --location eastus
   ```

4. **Create an App Service plan**:
   ```bash
   az appservice plan create --name codegen-mcp-plan --resource-group codegen-mcp-group --sku B1 --is-linux
   ```

5. **Create a web app**:
   ```bash
   az webapp create --resource-group codegen-mcp-group --plan codegen-mcp-plan --name codegen-mcp-app --runtime "PYTHON|3.9"
   ```

6. **Configure environment variables**:
   ```bash
   az webapp config appsettings set --resource-group codegen-mcp-group --name codegen-mcp-app --settings CODEGEN_ORG_ID=your-org-id CODEGEN_TOKEN=your-api-token
   ```

7. **Deploy the application**:
   ```bash
   az webapp up --name codegen-mcp-app --resource-group codegen-mcp-group
   ```

## Security Considerations

When deploying the Codegen Agent MCP server, consider the following security best practices:

### API Credentials Protection

1. **Environment Variables**: Always use environment variables for sensitive information like API credentials.
2. **Secret Management Services**: For cloud deployments, use platform-specific secret management services:
   - AWS: AWS Secrets Manager or Parameter Store
   - GCP: Secret Manager
   - Azure: Key Vault

3. **Rotation Policy**: Implement a regular rotation policy for API tokens.

### Network Security

1. **Firewall Rules**: Restrict access to the server using firewall rules.
2. **HTTPS**: Always use HTTPS for production deployments.
3. **Reverse Proxy**: Use a reverse proxy like Nginx or Traefik to handle SSL termination and additional security headers.

Example Nginx configuration:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Authentication and Authorization

1. **API Key Authentication**: Implement API key authentication for client requests.
2. **Rate Limiting**: Implement rate limiting to prevent abuse.
3. **IP Whitelisting**: Consider whitelisting trusted IP addresses.

### Container Security

1. **Non-root User**: Run the Docker container as a non-root user.
2. **Minimal Base Image**: Use minimal base images like `python:3.9-slim` or `alpine`.
3. **Image Scanning**: Regularly scan Docker images for vulnerabilities.

Example Dockerfile with non-root user:
```dockerfile
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

# Expose the port
EXPOSE 8000

# Run the server
CMD ["python", "examples/codegen_agent_server.py"]
```

## Environment Variable Configuration

The Codegen Agent MCP server uses environment variables for configuration. Here's a comprehensive list of environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CODEGEN_ORG_ID` | Codegen organization ID | "323" | Yes |
| `CODEGEN_TOKEN` | Codegen API token | "sk-ce027fa7-3c8d-4beb-8c86-ed8ae982ac99" | Yes |
| `MCP_HOST` | Host to bind the server | "127.0.0.1" | No |
| `MCP_PORT` | Port to bind the server | 8000 | No |
| `LOG_LEVEL` | Logging level | "INFO" | No |

### Setting Environment Variables

#### Linux/macOS:
```bash
export CODEGEN_ORG_ID="your-org-id"
export CODEGEN_TOKEN="your-api-token"
export MCP_HOST="0.0.0.0"
export MCP_PORT="8080"
export LOG_LEVEL="DEBUG"
```

#### Windows:
```cmd
set CODEGEN_ORG_ID=your-org-id
set CODEGEN_TOKEN=your-api-token
set MCP_HOST=0.0.0.0
set MCP_PORT=8080
set LOG_LEVEL=DEBUG
```

#### Docker:
```bash
docker run -d \
  --name codegen-mcp \
  -p 8080:8080 \
  -e CODEGEN_ORG_ID=your-org-id \
  -e CODEGEN_TOKEN=your-api-token \
  -e MCP_HOST=0.0.0.0 \
  -e MCP_PORT=8080 \
  -e LOG_LEVEL=INFO \
  codegen-mcp-server
```

### Using a .env File

For local development, you can use a `.env` file:

1. Create a `.env` file in the root directory:
   ```
   CODEGEN_ORG_ID=your-org-id
   CODEGEN_TOKEN=your-api-token
   MCP_HOST=0.0.0.0
   MCP_PORT=8080
   LOG_LEVEL=DEBUG
   ```

2. Install the python-dotenv package:
   ```bash
   pip install python-dotenv
   ```

3. Modify the server code to load the `.env` file:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Monitoring and Logging

Proper monitoring and logging are essential for maintaining a healthy production deployment.

### Logging Configuration

The Codegen Agent MCP server uses Python's built-in logging module. You can configure it by modifying the server code:

```python
import logging
import os

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("codegen_mcp.log")
    ]
)
```

### Monitoring Tools

1. **Prometheus and Grafana**: For metrics collection and visualization.
2. **ELK Stack**: For log aggregation and analysis.
3. **Cloud-native monitoring**:
   - AWS: CloudWatch
   - GCP: Cloud Monitoring
   - Azure: Azure Monitor

### Health Checks

Implement a health check endpoint to monitor the server's status:

```python
@mcp.resource("health")
def health_check():
    return {"status": "healthy"}
```

## Troubleshooting

Common issues and their solutions:

### Connection Refused

**Issue**: Clients cannot connect to the server.

**Solutions**:
- Ensure the server is running
- Check if the port is correctly exposed
- Verify firewall rules
- Make sure the server is binding to the correct host (use `0.0.0.0` to listen on all interfaces)

### Authentication Errors

**Issue**: API calls fail with authentication errors.

**Solutions**:
- Verify that `CODEGEN_ORG_ID` and `CODEGEN_TOKEN` are correctly set
- Check if the API token has expired
- Ensure the organization ID is valid

### Performance Issues

**Issue**: The server is slow or unresponsive.

**Solutions**:
- Increase server resources (CPU, memory)
- Implement caching for frequently used data
- Optimize database queries
- Consider horizontal scaling (multiple instances behind a load balancer)

### Docker Issues

**Issue**: Docker container exits unexpectedly.

**Solutions**:
- Check container logs: `docker logs codegen-mcp`
- Ensure the container has enough resources
- Verify that environment variables are correctly set
- Check for permission issues if using volumes

---

This deployment guide covers the essential aspects of deploying the Codegen Agent MCP server in different environments. For specific questions or issues, please refer to the project's documentation or create an issue on the GitHub repository.

