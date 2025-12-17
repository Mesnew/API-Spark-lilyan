"""
Configuration de la base de données MySQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Récupérer les paramètres MySQL depuis les variables d'environnement
MYSQL_USER = os.getenv("MYSQL_USER", "sirenuser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3366")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "siren")

# Construire l'URL de connexion MySQL
# Format: mysql+pymysql://user:password@host:port/database
MYSQL_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

print(f"Connecting to MySQL: {MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")

# Créer le moteur SQLAlchemy
engine = create_engine(MYSQL_URL, echo=True, pool_pre_ping=True, pool_recycle=3600)

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


def get_db():
    """
    Générateur de session de base de données
    À utiliser comme dépendance FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
