#!/usr/bin/env python3
"""
Script d'import de données CSV SIREN vers MySQL

Ce script importe un fichier CSV contenant des données d'unités légales
vers la base de données MySQL.

Usage:
    python import_csv_to_mysql.py [--csv-file PATH] [--batch-size SIZE]

Arguments:
    --csv-file      Chemin vers le fichier CSV (défaut: ../devAPI/data/StockUniteLegale_utf8.csv)
    --batch-size    Taille des lots d'insertion (défaut: 1000)
    --truncate      Vider la table avant l'import (défaut: False)
"""

import os
import sys
import argparse
import csv
import pymysql
from dotenv import load_dotenv
from typing import List, Dict, Any

# Charger les variables d'environnement
load_dotenv()

# Configuration MySQL depuis .env
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "sirenuser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "12345678")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "siren")

# Mapping des colonnes CSV vers les colonnes de la table
# Ajustez selon votre structure de CSV et de table
COLUMN_MAPPING = {
    'siren': 'siren',
    'statutDiffusionUniteLegale': 'statut_diffusion_unite_legale',
    'unitePurgeeUniteLegale': 'unite_purgee_unite_legale',
    'dateCreationUniteLegale': 'date_creation_unite_legale',
    'sigleUniteLegale': 'sigle_unite_legale',
    'sexeUniteLegale': 'sexe_unite_legale',
    'prenom1UniteLegale': 'prenom_1_unite_legale',
    'prenom2UniteLegale': 'prenom_2_unite_legale',
    'prenom3UniteLegale': 'prenom_3_unite_legale',
    'prenom4UniteLegale': 'prenom_4_unite_legale',
    'prenomUsuelUniteLegale': 'prenom_usuel_unite_legale',
    'pseudonymeUniteLegale': 'pseudonyme_unite_legale',
    'identifiantAssociationUniteLegale': 'identifiant_association_unite_legale',
    'trancheEffectifsUniteLegale': 'tranche_effectifs_unite_legale',
    'anneeEffectifsUniteLegale': 'annee_effectifs_unite_legale',
    'dateDernierTraitementUniteLegale': 'date_dernier_traitement_unite_legale',
    'nombrePeriodesUniteLegale': 'nombre_periodes_unite_legale',
    'categorieEntreprise': 'categorie_entreprise',
    'anneeCategorieEntreprise': 'annee_categorie_entreprise',
    'dateDebut': 'date_debut',
    'etatAdministratifUniteLegale': 'etat_administratif_unite_legale',
    'nomUniteLegale': 'nom_unite_legale',
    'nomUsageUniteLegale': 'nom_usage_unite_legale',
    'denominationUniteLegale': 'denomination_unite_legale',
    'denominationUsuelle1UniteLegale': 'denomination_usuelle_1_unite_legale',
    'denominationUsuelle2UniteLegale': 'denomination_usuelle_2_unite_legale',
    'denominationUsuelle3UniteLegale': 'denomination_usuelle_3_unite_legale',
    'categorieJuridiqueUniteLegale': 'categorie_juridique_unite_legale',
    'activitePrincipaleUniteLegale': 'activite_principale_unite_legale',
    'nomenclatureActivitePrincipaleUniteLegale': 'nomenclature_activite_principale_unite_legale',
    'nicSiegeUniteLegale': 'nic_siege_unite_legale',
    'economieSocialeSolidaireUniteLegale': 'economie_sociale_solidaire_unite_legale',
    'societeMissionUniteLegale': 'societe_mission_unite_legale',
    'caractereEmployeurUniteLegale': 'caractere_employeur_unite_legale'
}


def get_db_connection():
    """Créer une connexion à la base de données MySQL"""
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"✓ Connecté à MySQL {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
        return connection
    except Exception as e:
        print(f"✗ Erreur de connexion à MySQL: {e}")
        sys.exit(1)


def truncate_table(connection):
    """Vider la table unite_legale"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE unite_legale")
        connection.commit()
        print("✓ Table 'unite_legale' vidée")
    except Exception as e:
        print(f"✗ Erreur lors du vidage de la table: {e}")
        sys.exit(1)


def import_csv(csv_file: str, batch_size: int = 1000, truncate: bool = False):
    """
    Importer les données du CSV vers MySQL

    Args:
        csv_file: Chemin vers le fichier CSV
        batch_size: Nombre de lignes à insérer par lot
        truncate: Si True, vide la table avant l'import
    """
    if not os.path.exists(csv_file):
        print(f"✗ Fichier CSV non trouvé: {csv_file}")
        sys.exit(1)

    print(f"✓ Fichier CSV trouvé: {csv_file}")

    # Connexion à la base
    connection = get_db_connection()

    # Vider la table si demandé
    if truncate:
        truncate_table(connection)

    # Lire et importer le CSV
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Vérifier les colonnes
            csv_columns = reader.fieldnames
            print(f"✓ Colonnes CSV détectées: {len(csv_columns)} colonnes")

            batch = []
            total_rows = 0
            inserted_rows = 0
            skipped_rows = 0

            for row in reader:
                total_rows += 1

                # Mapper les colonnes CSV vers les colonnes de la table
                mapped_row = {}
                for csv_col, db_col in COLUMN_MAPPING.items():
                    value = row.get(csv_col, None)
                    # Convertir les chaînes vides en NULL
                    if value == '' or value is None:
                        mapped_row[db_col] = None
                    else:
                        mapped_row[db_col] = value

                batch.append(mapped_row)

                # Insérer par lots
                if len(batch) >= batch_size:
                    inserted = insert_batch(connection, batch)
                    inserted_rows += inserted
                    skipped_rows += len(batch) - inserted
                    print(f"  Traité {total_rows} lignes (insérées: {inserted_rows}, ignorées: {skipped_rows})")
                    batch = []

            # Insérer le dernier lot
            if batch:
                inserted = insert_batch(connection, batch)
                inserted_rows += inserted
                skipped_rows += len(batch) - inserted

            connection.commit()

            print("\n" + "="*60)
            print(f"✓ Import terminé avec succès!")
            print(f"  Total de lignes lues:     {total_rows}")
            print(f"  Lignes insérées:          {inserted_rows}")
            print(f"  Lignes ignorées (doublons): {skipped_rows}")
            print("="*60)

    except Exception as e:
        connection.rollback()
        print(f"\n✗ Erreur lors de l'import: {e}")
        sys.exit(1)
    finally:
        connection.close()


def insert_batch(connection, batch: List[Dict[str, Any]]) -> int:
    """
    Insérer un lot de lignes dans la table

    Args:
        connection: Connexion MySQL
        batch: Liste de dictionnaires représentant les lignes

    Returns:
        Nombre de lignes insérées
    """
    if not batch:
        return 0

    # Construire la requête INSERT
    columns = list(batch[0].keys())
    placeholders = ', '.join(['%s'] * len(columns))
    columns_str = ', '.join([f"`{col}`" for col in columns])

    query = f"""
        INSERT IGNORE INTO unite_legale ({columns_str})
        VALUES ({placeholders})
    """

    try:
        with connection.cursor() as cursor:
            # Préparer les valeurs
            values = [tuple(row[col] for col in columns) for row in batch]

            # Exécuter l'insertion
            inserted = cursor.executemany(query, values)

            return cursor.rowcount if cursor.rowcount > 0 else 0

    except Exception as e:
        print(f"  ⚠ Erreur lors de l'insertion d'un lot: {e}")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Importer des données CSV SIREN vers MySQL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python import_csv_to_mysql.py
  python import_csv_to_mysql.py --csv-file ./data/siren.csv
  python import_csv_to_mysql.py --batch-size 500 --truncate
        """
    )

    parser.add_argument(
        '--csv-file',
        default='../devAPI/data/StockUniteLegale_utf8.csv',
        help='Chemin vers le fichier CSV (défaut: ../devAPI/data/StockUniteLegale_utf8.csv)'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=1000,
        help='Taille des lots d\'insertion (défaut: 1000)'
    )

    parser.add_argument(
        '--truncate',
        action='store_true',
        help='Vider la table avant l\'import'
    )

    args = parser.parse_args()

    print("="*60)
    print("  IMPORT CSV VERS MYSQL - Données SIREN")
    print("="*60)
    print(f"Fichier CSV:     {args.csv_file}")
    print(f"Taille des lots: {args.batch_size}")
    print(f"Vider la table:  {'Oui' if args.truncate else 'Non'}")
    print(f"Base de données: {MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
    print("="*60 + "\n")

    import_csv(args.csv_file, args.batch_size, args.truncate)


if __name__ == "__main__":
    main()
