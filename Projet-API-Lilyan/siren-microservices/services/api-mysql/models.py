"""
Modèles SQLAlchemy pour la base de données SIREN
"""
from sqlalchemy import Column, String, Integer, Date
from database import Base


class UniteLegale(Base):
    """
    Table des unités légales (entreprises) - Version simplifiée pour tests
    """
    __tablename__ = "unite_legale"

    # Colonnes principales (correspondent à init-db.sql)
    siren = Column(String(9), primary_key=True, index=True)
    nom_unite_legale = Column(String(250), index=True)
    denomination_unite_legale = Column(String(250), index=True)
    activite_principale_unite_legale = Column(String(6), index=True)
    nomenclature_activite_principale_unite_legale = Column(String(8))
    tranche_effectifs_unite_legale = Column(String(2))
    date_creation = Column(Date)

    def to_dict(self):
        """
        Convertir en dictionnaire
        """
        return {
            "siren": self.siren,
            "nom": self.nom_unite_legale or self.denomination_unite_legale,
            "denomination": self.denomination_unite_legale,
            "activite_principale": self.activite_principale_unite_legale,
            "nomenclature_activite": self.nomenclature_activite_principale_unite_legale,
            "tranche_effectifs": self.tranche_effectifs_unite_legale,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }
