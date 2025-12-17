#!/bin/bash

# ============================================
# Script d'Arrêt Propre
# ============================================

echo "🛑 Arrêt du projet API Microservices..."
echo ""

# Arrêter tous les containers
docker-compose down

echo ""
echo "✅ Tous les services sont arrêtés!"
echo ""
echo "💡 Pour redémarrer:"
echo "  ./start.sh"
echo ""
echo "💡 Pour supprimer aussi les données:"
echo "  docker-compose down -v"
echo ""
