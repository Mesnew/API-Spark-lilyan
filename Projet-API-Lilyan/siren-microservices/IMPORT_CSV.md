# Import CSV vers MySQL

Script pour importer les données SIREN depuis un fichier CSV vers la base de données MySQL.

## Prérequis

1. La base de données MySQL doit être démarrée (via devAPI)
2. Python 3 avec les dépendances nécessaires

## Installation des dépendances

```bash
pip install pymysql python-dotenv
```

## Utilisation

### Import basique

```bash
python import_csv_to_mysql.py
```

Par défaut, le script importe le fichier `../devAPI/data/StockUniteLegale_utf8.csv`.

### Options disponibles

```bash
# Spécifier un fichier CSV différent
python import_csv_to_mysql.py --csv-file /chemin/vers/fichier.csv

# Modifier la taille des lots (par défaut: 1000)
python import_csv_to_mysql.py --batch-size 500

# Vider la table avant l'import
python import_csv_to_mysql.py --truncate

# Combiner plusieurs options
python import_csv_to_mysql.py --csv-file ./data/siren.csv --batch-size 2000 --truncate
```

## Configuration

Le script utilise les variables d'environnement du fichier `.env` :

```env
MYSQL_USER=sirenuser
MYSQL_PASSWORD=12345678
MYSQL_DATABASE=siren
MYSQL_HOST=localhost
MYSQL_PORT=3367
```

**Note :** Le port 3367 est le port exposé par devAPI qui redirige vers le port 3306 interne de MySQL.

## Fonctionnement

1. Le script lit le fichier CSV ligne par ligne
2. Mappe les colonnes CSV vers les colonnes de la table `unite_legale`
3. Insère les données par lots pour optimiser les performances
4. Ignore les doublons (SIREN déjà existants)
5. Affiche la progression et un résumé final

## Format CSV attendu

Le fichier CSV doit contenir les colonnes suivantes :

- `siren` (clé primaire)
- `statutDiffusionUniteLegale`
- `denominationUniteLegale`
- `activitePrincipaleUniteLegale`
- ... (et autres colonnes selon le schéma)

## Exemple de sortie

```
============================================================
  IMPORT CSV VERS MYSQL - Données SIREN
============================================================
Fichier CSV:     ../devAPI/data/StockUniteLegale_utf8.csv
Taille des lots: 1000
Vider la table:  Non
Base de données: sirenuser@localhost:3367/siren
============================================================

✓ Fichier CSV trouvé: ../devAPI/data/StockUniteLegale_utf8.csv
✓ Connecté à MySQL localhost:3367/siren
✓ Colonnes CSV détectées: 34 colonnes
  Traité 1000 lignes (insérées: 1000, ignorées: 0)
  Traité 2000 lignes (insérées: 2000, ignorées: 0)
  ...

============================================================
✓ Import terminé avec succès!
  Total de lignes lues:     5000
  Lignes insérées:          5000
  Lignes ignorées (doublons): 0
============================================================
```

## Dépannage

### Erreur de connexion MySQL

Si vous obtenez une erreur de connexion :

1. Vérifiez que devAPI est démarré : `cd ../devAPI && docker-compose ps`
2. Vérifiez le port : MySQL devrait être accessible sur `localhost:3367`
3. Vérifiez les credentials dans `.env`

### Erreur "File not found"

Vérifiez que le fichier CSV existe :

```bash
ls -la ../devAPI/data/StockUniteLegale_utf8.csv
```

### Colonnes manquantes

Si le CSV a un format différent, ajustez le `COLUMN_MAPPING` dans `import_csv_to_mysql.py`.

## Performance

- **Taille des lots recommandée** : 1000-2000 lignes
- **Temps estimé** : ~1-2 secondes par 1000 lignes
- **Utilisation mémoire** : Faible (traitement par lots)

## Sécurité

- Le script utilise `INSERT IGNORE` pour éviter les erreurs de doublons
- Les valeurs NULL sont gérées automatiquement
- Les transactions sont utilisées pour garantir la cohérence
- En cas d'erreur, un rollback est effectué
