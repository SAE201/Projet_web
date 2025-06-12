-- ┌────────────────────────────────────────────────┐
-- │  Base_donnee.sql : schéma des tables statiques │
-- └────────────────────────────────────────────────┘

-- Table Département
CREATE TABLE IF NOT EXISTS Departement (
    code_departement TEXT PRIMARY KEY,
    nom_departement  TEXT
);

-- Table Distributeur (UGE / MOA)
CREATE TABLE IF NOT EXISTS Distributeur (
    nom_uge          TEXT PRIMARY KEY,
    nom_distributeur TEXT,
    nom_moa          TEXT
);

-- Table Commune
CREATE TABLE IF NOT EXISTS Commune (
    code_commune     TEXT PRIMARY KEY,
    nom_commune      TEXT,
    code_departement TEXT,
    nom_departement  TEXT,
    nom_uge          TEXT,
    nom_distributeur TEXT,
    nom_moa          TEXT,
    FOREIGN KEY(code_departement) REFERENCES Departement(code_departement),
    FOREIGN KEY(nom_uge)          REFERENCES Distributeur(nom_uge)
);

-- Table Réseau (UDI)
CREATE TABLE IF NOT EXISTS Reseau (
    code_reseau   TEXT PRIMARY KEY,
    nom_reseau    TEXT,
    nom_quartier  TEXT,
    debut_alim    DATE,
    annee         TEXT,
    code_commune  TEXT,
    nom_uge       TEXT,
    FOREIGN KEY(code_commune) REFERENCES Commune(code_commune),
    FOREIGN KEY(nom_uge)       REFERENCES Distributeur(nom_uge)
);

-- Table Parametre (référentiel SANDRE / SISE-Eaux)
-- (reste vide en SAE 2.04, mais doit être créée dans le schéma)
CREATE TABLE IF NOT EXISTS Parametre (
    code_parametre           TEXT PRIMARY KEY,
    code_parametre_se        TEXT,
    code_parametre_cas       TEXT,
    libelle_parametre        TEXT,
    libelle_parametre_maj    TEXT,
    code_type_parametre      TEXT,
    libelle_unite            TEXT,
    code_unite               TEXT,
    limite_qualite_parametre TEXT
);
