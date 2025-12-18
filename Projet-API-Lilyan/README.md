# Projet API SIREN - Déploiement Simple

APIs REST pour gérer les données des entreprises françaises.

## Installation

### 1. Cloner le projet

```bash
git clone git@github.com:Mesnew/API-Spark-Lilyan.git
cd API-Spark-Lilyan/Projet-API-Lilyan
```

### 2. Créer le fichier .env

```bash
cd siren-microservices
cp .env.example .env
```

**Contenu du fichier .env (déjà configuré) :**

```env
OAUTH2_CLIENT_ID=client-app
OAUTH2_CLIENT_SECRET=Dev_Client_Secret_2024!
OAUTH2_USER1=user1:DevUser1Pass2024!
OAUTH2_USER2=user2:DevUser2Pass2024!

MYSQL_USER=root
MYSQL_PASSWORD=rootpassword
MYSQL_DATABASE=siren_db
```

### 3. Démarrer l'infrastructure

```bash
cd ../devAPI
docker-compose up -d
```

Attendre **2 minutes**.

### 4. Démarrer les APIs

```bash
cd ../siren-microservices
docker-compose up -d
```

### 5. Configurer les noms de domaine locaux

**IMPORTANT** : Les APIs utilisent Nginx avec des noms de domaine virtuels. Vous devez configurer votre fichier `/etc/hosts` :

```bash
sudo nano /etc/hosts
```

Ajoutez ces lignes à la fin du fichier :

```
127.0.0.1 oauth.siren.local
127.0.0.1 mysql.siren.local
127.0.0.1 spark.siren.local
```

Sauvegardez (`Ctrl+O`, `Entrée`, `Ctrl+X`).

## ✅ C'est prêt !

Vérifier :
```bash
docker-compose ps
```

Tester :
```bash
./test_reverse_proxy.sh
```

## Accès

- **OAuth2** : http://oauth.siren.local/api-docs
- **API MySQL** : http://mysql.siren.local/docs
- **API Spark** : http://spark.siren.local/docs

## Obtenir un token

### Option 1 : Swagger UI

1. Aller sur http://oauth.siren.local/api-docs
2. Endpoint `POST /v1/oauth/token`
3. Cliquer "Try it out"
4. Remplir :
   - username: `user1`
   - password: `DevUser1Pass2024!`
   - client_id: `client-app`
   - client_secret: `Dev_Client_Secret_2024!`
   - grant_type: `password`
5. Copier le `access_token`

### Option 2 : Terminal

```bash
curl -X POST http://oauth.siren.local/v1/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=user1&password=DevUser1Pass2024!&client_id=client-app&client_secret=Dev_Client_Secret_2024!"
```

## Tester les APIs

Remplacer `VOTRE_TOKEN` par le token obtenu :

```bash
# API MySQL - Recherche par nom
curl -H "Authorization: Bearer VOTRE_TOKEN" \
  "http://mysql.siren.local/v1/entreprises/search?nom=TEST"

# API Spark - Top 10 activités
curl -H "Authorization: Bearer VOTRE_TOKEN" \
  "http://spark.siren.local/v1/stats/activites/top?limit=10"
```

## Arrêter

```bash
cd siren-microservices
docker-compose down

cd ../devAPI
docker-compose down
```

## Identifiants

- Username: `user1`
- Password: `DevUser1Pass2024!`
- Client ID: `client-app`
- Client Secret: `Dev_Client_Secret_2024!`
