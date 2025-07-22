FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster Python package management
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY src/ ./src/

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Create directory for credentials
RUN mkdir -p /app/config

# Environment variables
ENV SERVICE_ACCOUNT_PATH=/app/config/service-account.json
ENV DRIVE_FOLDER_ID=""
ENV PYTHONPATH=/app/src
ENV FASTMCP_PORT=8004
ENV FASTMCP_HOST=0.0.0.0

# Expose MCP port
EXPOSE 8004

# Command to run the MCP server
CMD ["uv", "run", "mcp-google-sheets"]
