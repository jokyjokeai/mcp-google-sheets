FROM python:3.11-slim

WORKDIR /app

# Installer uv
RUN pip install uv

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Installer mcp-google-sheets
RUN uv pip install mcp-google-sheets

# Copier l'application
COPY app.py .

# Créer le dossier credentials
RUN mkdir -p /app/credentials

EXPOSE 8003

CMD ["python", "app.py"]
