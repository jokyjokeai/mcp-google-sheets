FROM python:3.11-slim

# Installer les dépendances
RUN pip install flask flask-cors uv

# Installer MCP Google Sheets
RUN uv pip install mcp-google-sheets

# Créer le répertoire de travail
WORKDIR /app

# Copier le wrapper HTTP (à créer)
COPY http_wrapper.py .

# Créer le dossier pour les credentials
RUN mkdir -p /app/credentials

# Exposer le port
EXPOSE 8003

# Lancer le wrapper
CMD ["python", "http_wrapper.py"]
