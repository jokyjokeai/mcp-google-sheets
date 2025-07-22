FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
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

# Expose MCP default port
EXPOSE 8000

# Command to run the MCP server
CMD ["uv", "run", "mcp-google-sheets"]
