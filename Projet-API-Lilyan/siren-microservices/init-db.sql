-- ============================================
-- Initialisation Base de Données SIREN
-- ============================================

-- Créer la base de données si elle n'existe pas
CREATE DATABASE IF NOT EXISTS siren CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE siren;

-- Supprimer la table si elle existe déjà
DROP TABLE IF EXISTS unite_legale;

-- Créer la table unite_legale
CREATE TABLE unite_legale (
    siren CHAR(9) NOT NULL,
    nom_unite_legale VARCHAR(250) NULL,
    denomination_unite_legale VARCHAR(250) NULL,
    activite_principale_unite_legale CHAR(6) NULL,
    nomenclature_activite_principale_unite_legale VARCHAR(8) NULL,
    tranche_effectifs_unite_legale VARCHAR(2) NULL,
    date_creation DATE NULL,

    PRIMARY KEY (siren),
    INDEX idx_denomination (denomination_unite_legale),
    INDEX idx_nom (nom_unite_legale),
    INDEX idx_activite (activite_principale_unite_legale)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insérer des données de test
INSERT INTO unite_legale (
    siren,
    nom_unite_legale,
    denomination_unite_legale,
    activite_principale_unite_legale,
    nomenclature_activite_principale_unite_legale,
    tranche_effectifs_unite_legale,
    date_creation
) VALUES
    ('123456789', NULL, 'ENTREPRISE TEST 1', '62.01Z', 'NAFRev2', '01', '2020-01-15'),
    ('987654321', NULL, 'ENTREPRISE TEST 2', '62.01Z', 'NAFRev2', '02', '2019-05-20'),
    ('111222333', NULL, 'AUTRE ENTREPRISE', '47.11F', 'NAFRev2', '03', '2021-03-10'),
    ('444555666', NULL, 'SOCIETE EXEMPLE', '62.01Z', 'NAFRev2', '01', '2018-11-25'),
    ('777888999', NULL, 'COMMERCE DE DETAIL', '47.11F', 'NAFRev2', '02', '2022-07-08'),
    ('555666777', NULL, 'SERVICES INFORMATIQUES', '62.02A', 'NAFRev2', '01', '2020-09-12'),
    ('333444555', NULL, 'DEVELOPPEMENT WEB', '62.01Z', 'NAFRev2', '00', '2021-06-30'),
    ('666777888', NULL, 'CONSEIL STRATEGIE', '70.22Z', 'NAFRev2', '01', '2019-02-14'),
    ('222333444', NULL, 'FORMATION PROFESSIONNELLE', '85.59A', 'NAFRev2', '02', '2020-11-05'),
    ('888999000', NULL, 'RESTAURATION RAPIDE', '56.10C', 'NAFRev2', '03', '2022-01-20'),
    ('100200300', NULL, 'BOULANGERIE ARTISANALE', '10.71C', 'NAFRev2', '01', '2018-04-15'),
    ('200300400', NULL, 'AGENCE COMMUNICATION', '73.11Z', 'NAFRev2', '01', '2021-08-22'),
    ('300400500', NULL, 'TRANSPORT ROUTIER', '49.41A', 'NAFRev2', '02', '2019-12-10'),
    ('400500600', NULL, 'NETTOYAGE INDUSTRIEL', '81.22Z', 'NAFRev2', '03', '2020-05-18'),
    ('500600700', NULL, 'ARCHITECTE', '71.11Z', 'NAFRev2', '00', '2021-02-28'),
    ('600700800', NULL, 'PHARMACIE', '47.73Z', 'NAFRev2', '01', '2017-09-05'),
    ('700800900', NULL, 'COIFFURE', '96.02A', 'NAFRev2', '00', '2022-03-14'),
    ('800900100', NULL, 'PLOMBERIE', '43.22A', 'NAFRev2', '01', '2020-10-20'),
    ('900100200', NULL, 'ELECTRICITE', '43.21A', 'NAFRev2', '02', '2019-07-25'),
    ('100300500', NULL, 'MENUISERIE', '16.23Z', 'NAFRev2', '01', '2021-11-08');

-- Afficher le résultat
SELECT
    COUNT(*) as total_entreprises,
    COUNT(DISTINCT activite_principale_unite_legale) as total_activites
FROM unite_legale;

SELECT
    activite_principale_unite_legale as code_activite,
    COUNT(*) as nombre_entreprises
FROM unite_legale
GROUP BY activite_principale_unite_legale
ORDER BY nombre_entreprises DESC
LIMIT 5;
