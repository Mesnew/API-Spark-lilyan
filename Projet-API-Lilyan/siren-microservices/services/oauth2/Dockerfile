# =========================================
# Dockerfile pour l'API OAuth2 (Node.js/Express)
# =========================================

FROM node:18-alpine

WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install --production

# Copier le code de l'application
COPY . .

# Exposer le port
EXPOSE 3000

# Commande de démarrage
CMD ["node", "app.js"]
