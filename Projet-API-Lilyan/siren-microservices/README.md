# Architecture Microservices SIREN

Architecture conteneurisée de 2 services API pour la gestion et l'analyse des données SIREN (entreprises françaises).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   ARCHITECTURE GLOBALE                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   Client        │
│  (Postman)      │
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         v              v
┌────────────────┐  ┌────────────────┐
│  API OAuth2    │  │   API MySQL    │
│  (Express.js)  │  │  (FastAPI)     │
│  Port: 3000    │  │  Port: 3001    │
│                │  │                │
│  - Auth        │  │  - Entreprises │
│  - Tokens      │  │  - SIREN       │
│  - Swagger     │  │  - Recherche   │
└────────────────┘  └───────┬────────┘
                            │
                            v
                    ┌───────────────┐
                    │  MySQL 8.0    │
                    │  Port: 3366   │
                    │               │
                    │  DB: siren    │
                    └───────────────┘
```

## Services

### 1. API OAuth2 (Node.js + Express)
**Port:** 3000
**Technologie:** Node.js, Express, express-oauth-server

**Endpoints:**
- `POST /oauth/token` - Obtenir un token
- `GET /secure` - Route protégée exemple
- `GET /me` - Informations utilisateur
- `GET /users` - Liste des utilisateurs
- `GET /health` - Santé du service

**Documentation:** http://localhost:3000/api-docs

### 2. API MySQL (Python + FastAPI)
**Port:** 3001
**Technologie:** Python 3.11, FastAPI, SQLAlchemy, MySQL

**Endpoints:**
- `GET /entreprises/siren/{siren}` - Entreprise par SIREN
- `GET /entreprises/activite/{code}` - Entreprises par code activité
- `GET /entreprises/search` - Recherche par nom
- `GET /health` - Santé du service

**Fonctionnalités:**
- Pagination (20 par défaut, paramétrable)
- Format JSON-LD
- Documentation Swagger automatique
- Protection OAuth2

**Documentation:** http://localhost:3001/docs

### 3. MySQL Database
**Port:** 3366
**Image:** mysql:8.0

Base de données contenant les informations des entreprises françaises (SIREN).

## Exigences respectées

- [x] 2 services API distincts
- [x] Conteneurisation Docker
- [x] Documentation Swagger pour chaque API
- [x] Format JSON-LD
- [x] Pagination (20 par défaut, paramétrable)
- [x] Protection OAuth2
- [x] Technologies variées (Node.js, Python)
- [x] Testable avec Postman

## Installation

### Prérequis

- Docker & Docker Compose
- Fichier de données SIREN (voir ci-dessous)

### Configuration des variables d'environnement (IMPORTANT)

**🔒 Sécurité:** Ce projet utilise des variables d'environnement pour gérer les credentials de manière sécurisée.

#### Première installation

1. **Copier le fichier d'exemple:**
```bash
cp .env.example .env
```

2. **Modifier le fichier .env avec des valeurs sécurisées:**
```bash
nano .env  # ou votre éditeur préféré
```

3. **Générer des mots de passe forts** (recommandé pour production):
```bash
# Exemple avec openssl
openssl rand -base64 32
```

#### Variables à configurer

| Variable | Description | Exemple |
|----------|-------------|---------|
| `MYSQL_ROOT_PASSWORD` | Mot de passe root MySQL | `Strong_Root_Pass_2024!` |
| `MYSQL_PASSWORD` | Mot de passe utilisateur MySQL | `Strong_User_Pass_2024!` |
| `OAUTH2_CLIENT_SECRET` | Secret du client OAuth2 | `Strong_Client_Secret_2024!` |
| `OAUTH2_USER1` | Premier utilisateur (username:password) | `user1:StrongPass1!` |
| `OAUTH2_USER2` | Deuxième utilisateur (username:password) | `user2:StrongPass2!` |

**⚠️ ATTENTION:**
- **JAMAIS** committer le fichier `.env` dans git (déjà dans `.gitignore`)
- Utiliser des mots de passe différents pour chaque environnement (dev/prod)
- En production, utiliser un gestionnaire de secrets (Vault, Kubernetes Secrets, etc.)

#### Fichiers fournis

- **`.env.example`**: Template avec toutes les variables requises
- **`.env`**: Fichier local avec vos valeurs (à créer, git-ignoré)

### Téléchargement des données

```bash
cd data
wget https://object.files.data.gouv.fr/data-pipeline-open/siren/stock/StockUniteLegale_utf8.zip
unzip StockUniteLegale_utf8.zip
```

### Démarrage

```bash
# Lancer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

### Initialisation de la base de données

```bash
# Attendre que MySQL soit prêt
docker-compose exec db mysqladmin ping

# Charger les données de test
docker-compose exec -T db mysql -usirenuser -pDev_Siren_Pass_2024! < init-db.sql
```

## Utilisation

### 1. Obtenir un token OAuth2

**Note:** Utilisez les credentials définis dans votre fichier `.env`

```bash
# Avec les credentials par défaut du .env de développement
curl -X POST http://localhost:3000/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "username=user1" \
  -d "password=DevUser1Pass2024!" \
  -d "client_id=client-app" \
  -d "client_secret=Dev_Client_Secret_2024!"
```

### 2. Utiliser le token pour accéder aux APIs

```bash
# API MySQL - Rechercher une entreprise
curl -X GET http://localhost:3001/entreprises/siren/123456789 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Tester avec Swagger

- OAuth2: http://localhost:3000/api-docs
- API MySQL: http://localhost:3001/docs

## Credentials de développement

**⚠️ Ces credentials sont définis dans le fichier `.env`**

**Valeurs par défaut (fichier .env fourni):**
- **Client ID:** `client-app`
- **Client Secret:** `Dev_Client_Secret_2024!`
- **User1:** `user1` / `DevUser1Pass2024!`
- **User2:** `user2` / `DevUser2Pass2024!`

**🔒 Pour la production:**
- Modifier TOUS les mots de passe dans `.env`
- Ne JAMAIS utiliser les valeurs par défaut en production
- Utiliser un gestionnaire de secrets sécurisé

## Structure du projet

```
siren-microservices/
├── docker-compose.yml          # Orchestration des services
├── .env                        # Variables d'environnement
├── README.md                   # Ce fichier
├── data/                       # Données SIREN
│   └── StockUniteLegale_utf8.csv
├── docs/                       # Documentation
│   ├── postman-collection.json
│   └── architecture.md
└── services/
    ├── oauth2/                 # API OAuth2 (Node.js)
    │   ├── Dockerfile
    │   ├── package.json
    │   ├── app.js
    │   ├── model.js
    │   └── swagger.js
    └── api-mysql/              # API MySQL (Python/FastAPI)
        ├── Dockerfile
        ├── requirements.txt
        ├── main.py
        ├── models.py
        ├── schemas.py
        └── database.py
```

## JSON-LD Format

Toutes les réponses des APIs suivent le format JSON-LD avec contexte :

```json
{
  "@context": "https://schema.org/",
  "@type": "Organization",
  "@id": "siren:123456789",
  "identifier": "123456789",
  "name": "ENTREPRISE EXEMPLE",
  "address": {...}
}
```

## Pagination

Tous les endpoints supportent la pagination :

```
GET /entreprises/search?nom=test&page=1&limit=50
```

- `page`: Numéro de page (défaut: 1)
- `limit`: Nombre d'éléments (défaut: 20, max: 100)

## Développement

### Ajouter un nouveau service

1. Créer un dossier dans `services/`
2. Ajouter un `Dockerfile`
3. Configurer dans `docker-compose.yml`
4. Implémenter l'authentification OAuth2
5. Ajouter la documentation Swagger
6. Implémenter JSON-LD

### Tests

```bash
# Lancer les tests
docker-compose exec api-mysql pytest
```

## Monitoring

- Logs: `docker-compose logs -f [service]`
- Health checks: Endpoint `/health` sur chaque service
- Métriques: TODO (Prometheus + Grafana)

## Sécurité

- Tous les endpoints (sauf OAuth2) sont protégés par tokens
- HTTPS recommandé en production
- Rate limiting à implémenter
- Secrets à externaliser (.env, vault)

## Licence

ISC
