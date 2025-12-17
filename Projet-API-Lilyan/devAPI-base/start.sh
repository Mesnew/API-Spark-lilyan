#!/bin/bash

# ============================================
# Script de Démarrage Automatique
# ============================================

set -e

echo "🚀 Démarrage du projet API Microservices..."
echo ""

# Démarrer MySQL d'abord
echo "1️⃣  Démarrage de MySQL..."
docker-compose up -d db

echo "⏳ Attente de MySQL (30 secondes)..."
sleep 30

# Charger les données
echo "2️⃣  Chargement des données de test..."
docker exec -i mysql8 mysql -uroot -p12345678 siren < init-db.sql 2>/dev/null

# Démarrer tous les services
echo "3️⃣  Démarrage de tous les services..."
docker-compose up -d

echo ""
echo "✅ Projet démarré avec succès!"
echo ""
echo "📊 Containers en cours d'exécution:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "📝 Documentation Swagger:"
echo "  - OAuth2:    http://localhost:3000/api-docs"
echo "  - API MySQL: http://localhost:3001/docs"
echo "  - API Spark: http://localhost:3002/api-docs"
echo ""
echo "💡 Commandes utiles:"
echo "  - Voir les logs:  docker-compose logs -f"
echo "  - Arrêter:        docker-compose down"
echo "  - Redémarrer:     docker-compose restart"
echo ""
