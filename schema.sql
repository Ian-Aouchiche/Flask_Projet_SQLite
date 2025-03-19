-- Suppression des tables existantes si elles existent
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Stocks;
DROP TABLE IF EXISTS Borrowings;

-- Création de la table des rôles (Admin / Utilisateur)
CREATE TABLE IF NOT EXISTS Roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_role TEXT UNIQUE NOT NULL
);

-- Création de la table des utilisateurs
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE
);

-- Création de la table des livres
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    annee_publication INTEGER,
    genre TEXT,
    isbn TEXT UNIQUE NOT NULL
);

-- Création de la table des stocks
CREATE TABLE IF NOT EXISTS Stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livre_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL CHECK (quantite >= 0),
    emplacement TEXT,
    FOREIGN KEY (livre_id) REFERENCES Books(id) ON DELETE CASCADE
);

-- Création de la table des emprunts
CREATE TABLE IF NOT EXISTS Borrowings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    livre_id INTEGER NOT NULL,
    date_emprunt DATE NOT NULL,
    date_retour DATE,
    retourne BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (utilisateur_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (livre_id) REFERENCES Books(id) ON DELETE CASCADE
);
