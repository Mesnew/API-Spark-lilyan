# =========================================
# Dockerfile pour l'API MySQL (FastAPI)
# =========================================

FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port
EXPOSE 3001

# Variables d'environnement par défaut (seront overridées par docker-compose)
ENV OAUTH2_URL="http://oauth2:3000"

# Note: Les credentials MySQL sont passés via docker-compose.yaml
# Ne JAMAIS hardcoder de credentials dans les Dockerfiles

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001", "--reload"]
