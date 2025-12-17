# 🚀 Projet API Microservices - Lilyan

Architecture microservices complète avec 3 APIs REST + Spark Analytics

---

## 📋 Table des Matières

- [Vue d'Ensemble](#-vue-densemble)
- [Prérequis](#-prérequis)
- [Installation Rapide](#-installation-rapide)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [APIs Disponibles](#-apis-disponibles)
- [Dépannage](#-dépannage)

---

## 🎯 Vue d'Ensemble

Ce projet contient **5 services Docker** :

1. **MySQL 8.0** - Base de données
2. **Spark Connect** - Serveur d'analyse (Scala)
3. **API OAuth2** - Authentification (Node.js)
4. **API MySQL** - Recherche d'entreprises (Python FastAPI)
5. **API Spark** - Statistiques agrégées (Node.js)

**Technologies :** Docker, Node.js, Python, MySQL, Spark, OAuth2, JSON-LD, Hydra

---

## ✅ Prérequis

Avant de commencer, assure-toi d'avoir :

- [x] **Docker** version 20.10+
- [x] **Docker Compose** version 2.0+
- [x] **8 Go de RAM minimum**
- [x] **Ports libres** : 3000, 3001, 3002, 3367, 15002

### Vérifier les prérequis

```bash
docker --version
docker-compose --version
```

---

## 🚀 Installation Rapide

### Étape 1 : Ouvrir le terminal dans ce dossier

```bash
cd /chemin/vers/devAPI-base
```

### Étape 2 : Démarrer tous les services

```bash
# Démarrer MySQL d'abord
docker-compose up -d db

# Attendre que MySQL soit prêt (30 secondes)
sleep 30

# Charger les données de test
docker exec -i mysql8 mysql -uroot -p12345678 siren < init-db.sql

# Démarrer tous les autres services
docker-compose up -d
```

### Étape 3 : Vérifier que tout fonctionne

```bash
# Voir les containers
docker ps

# Tu dois avoir 5 containers : mysql8, spark, siren-oauth2, siren-api-mysql, siren-api-spark
```

**✅ C'EST FAIT ! Tes APIs sont prêtes.**

---

## 🎮 Utilisation

### 1. Obtenir un Token OAuth2

```bash
curl -X POST http://localhost:3000/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "username=user1" \
  -d "password=DevUser1Pass2024!" \
  -d "client_id=client-app" \
  -d "client_secret=Dev_Client_Secret_2024!"
```

**Réponse :**
```json
{
  "access_token": "ton_token_ici",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### 2. Utiliser les APIs avec le Token

```bash
# Remplace TON_TOKEN par le token obtenu
TOKEN="ton_token_ici"

# Rechercher une entreprise par SIREN
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3001/entreprises/siren/123456789

# Obtenir des statistiques
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:3002/stats/activites/count?page=1&limit=5"
```

### 3. Accéder aux Documentations Swagger

Ouvre ton navigateur :

- **OAuth2 Swagger :** http://localhost:3000/api-docs
- **API MySQL (FastAPI) :** http://localhost:3001/docs
- **API Spark Swagger :** http://localhost:3002/api-docs

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  OAuth2  │  │   API    │  │   API    │             │
│  │  :3000   │  │  MySQL   │  │  Spark   │             │
│  │          │  │  :3001   │  │  :3002   │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │             │                     │
│       └─────────────┴─────────────┘                     │
│                     │                                    │
│              ┌──────▼──────┐                            │
│              │   MySQL     │                            │
│              │   :3367     │                            │
│              └─────────────┘                            │
│                                                          │
│              ┌─────────────┐                            │
│              │Spark Connect│                            │
│              │   :15002    │                            │
│              └─────────────┘                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🌐 APIs Disponibles

### API OAuth2 (Port 3000)

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/oauth/token` | POST | Générer un token |
| `/secure` | GET | Route protégée (test) |
| `/me` | GET | Info utilisateur |
| `/health` | GET | Health check |

### API MySQL (Port 3001)

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/entreprises/siren/{siren}` | GET | Recherche par SIREN |
| `/entreprises/activite/{code}` | GET | Recherche par code activité |
| `/entreprises/search?nom=xxx` | GET | Recherche par nom |
| `/health` | GET | Health check |

### API Spark (Port 3002)

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/stats/activites/count?page=1&limit=20` | GET | Statistiques paginées |
| `/stats/activites/filter?code=62.01Z` | GET | Filtre par code |
| `/stats/activites/top?limit=5` | GET | Top 5 codes |
| `/stats/activites/bottom?limit=5` | GET | Bottom 5 codes |
| `/health` | GET | Health check |

**Format des réponses :** JSON-LD avec Hydra (pagination hypermedia)

---

## 🔧 Commandes Utiles

### Démarrage et Arrêt

```bash
# Démarrer tout
docker-compose up -d

# Arrêter tout
docker-compose down

# Arrêter et supprimer les données
docker-compose down -v
```

### Logs et Debug

```bash
# Voir tous les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f siren-api-spark

# Voir l'état des services
docker ps
```

### Redémarrage

```bash
# Redémarrer tous les services
docker-compose restart

# Redémarrer un service spécifique
docker-compose restart siren-api-mysql
```

### Base de Données

```bash
# Se connecter à MySQL
docker exec -it mysql8 mysql -uroot -p12345678 siren

# Voir les données
docker exec mysql8 mysql -uroot -p12345678 siren -e "SELECT * FROM unite_legale LIMIT 5;"

# Recharger les données
docker exec -i mysql8 mysql -uroot -p12345678 siren < init-db.sql
```

---

## 🐛 Dépannage

### Problème : Container Spark crash au démarrage

**Erreur :** `Table 'siren.unite_legale' doesn't exist`

**Solution :**
```bash
# Charger les données d'abord
docker exec -i mysql8 mysql -uroot -p12345678 siren < init-db.sql

# Redémarrer Spark
docker-compose restart spark
```

### Problème : Port déjà utilisé

**Erreur :** `port is already allocated`

**Solution :**
```bash
# Arrêter tous les containers Docker
docker-compose down

# Vérifier qu'aucun port n'est utilisé
sudo lsof -i :3000
sudo lsof -i :3001
sudo lsof -i :3002

# Redémarrer
docker-compose up -d
```

### Problème : Services "unhealthy"

**Solution :** C'est normal au démarrage ! Attends 30-60 secondes et vérifie à nouveau :

```bash
docker ps
```

Les status doivent passer de "starting" à "healthy".

### Problème : Pas de réponse des APIs

**Solution :**
```bash
# Vérifier les logs
docker-compose logs siren-api-mysql
docker-compose logs siren-api-spark

# Vérifier que MySQL est prêt
docker exec mysql8 mysql -uroot -p12345678 siren -e "SELECT COUNT(*) FROM unite_legale;"
```

### Problème : Build prend trop de temps (5+ minutes)

**Solution :** Utilise le mode développement avec volumes :

```bash
# Utiliser docker-compose.dev.yaml
docker-compose -f docker-compose.dev.yaml up -d

# OU utiliser le script rapide
./dev.sh
```

Voir `FAST_START.md` pour plus de détails.

---

## 📚 Fichiers Importants

```
devAPI-base/
├── README.md                  ← Ce fichier
├── README_INTEGRATION.md      ← Documentation technique complète
├── FAST_START.md              ← Optimisations de build
├── docker-compose.yaml        ← Configuration production
├── docker-compose.dev.yaml    ← Configuration développement
├── init-db.sql                ← Données de test (20 entreprises)
├── dev.sh                     ← Script de démarrage rapide
└── services/
    ├── oauth2/                ← API OAuth2 (Node.js)
    ├── api-mysql/             ← API MySQL (Python)
    └── api-spark/             ← API Spark (Node.js)
```

---

## 🔐 Credentials (Développement Seulement)

### OAuth2
- **Client ID :** `client-app`
- **Client Secret :** `Dev_Client_Secret_2024!`
- **User 1 :** `user1` / `DevUser1Pass2024!`
- **User 2 :** `user2` / `DevUser2Pass2024!`

### MySQL
- **Host :** `localhost:3367`
- **Root Password :** `12345678`
- **User :** `sirenuser`
- **Password :** `12345678`
- **Database :** `siren`

⚠️ **ATTENTION :** Ces credentials sont pour le développement uniquement !

---

## ⚡ Script de Démarrage Automatique

Crée un fichier `start.sh` :

```bash
#!/bin/bash
echo "🚀 Démarrage du projet..."

# Démarrer MySQL
docker-compose up -d db
sleep 30

# Charger les données
docker exec -i mysql8 mysql -uroot -p12345678 siren < init-db.sql

# Démarrer tous les services
docker-compose up -d

echo "✅ Projet démarré!"
echo ""
echo "📝 Documentation Swagger:"
echo "  - OAuth2:    http://localhost:3000/api-docs"
echo "  - API MySQL: http://localhost:3001/docs"
echo "  - API Spark: http://localhost:3002/api-docs"
```

Puis :
```bash
chmod +x start.sh
./start.sh
```

---

## 📞 Support

Si tu as des problèmes :

1. Vérifie les logs : `docker-compose logs -f`
2. Vérifie que MySQL a les données : `docker exec mysql8 mysql -uroot -p12345678 siren -e "SELECT COUNT(*) FROM unite_legale;"`
3. Redémarre tout : `docker-compose down && docker-compose up -d`
4. Consulte `README_INTEGRATION.md` pour plus de détails

---

## 🎯 Résumé des Commandes Essentielles

```bash
# 1. DÉMARRER
docker-compose up -d db
sleep 30
docker exec -i mysql8 mysql -uroot -p12345678 siren < init-db.sql
docker-compose up -d

# 2. OBTENIR UN TOKEN
curl -X POST http://localhost:3000/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=user1&password=DevUser1Pass2024!&client_id=client-app&client_secret=Dev_Client_Secret_2024!"

# 3. UTILISER LES APIs (avec ton token)
TOKEN="ton_token"
curl -H "Authorization: Bearer $TOKEN" http://localhost:3001/entreprises/siren/123456789

# 4. ARRÊTER
docker-compose down
```

---

**Bon développement ! 🚀**

Pour plus de détails techniques, voir `README_INTEGRATION.md`.
