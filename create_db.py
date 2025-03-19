import sqlite3

# Connexion à la base de données SQLite (créera database.db si elle n'existe pas)
connection = sqlite3.connect('database.db')

# Lecture et exécution du fichier schema.sql
with open('schema.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion des rôles (Admin et Utilisateur)
cur.execute("INSERT INTO Roles (nom_role) VALUES (?)", ('Admin',))
cur.execute("INSERT INTO Roles (nom_role) VALUES (?)", ('Utilisateur',))

# Insertion d'un administrateur par défaut (le mot de passe doit être haché en production)
cur.execute("INSERT INTO Users (nom, email, mot_de_passe, role_id) VALUES (?, ?, ?, ?)", 
            ('Admin Principal', 'admin@biblio.com', 'motdepassehaché', 1))

# Insertion de quelques utilisateurs normaux
cur.execute("INSERT INTO Users (nom, email, mot_de_passe, role_id) VALUES (?, ?, ?, ?)", 
            ('Dupont Emilie', 'emilie.dupont@mail.com', '123456', 2))
cur.execute("INSERT INTO Users (nom, email, mot_de_passe, role_id) VALUES (?, ?, ?, ?)", 
            ('Martin Amandine', 'amandine.martin@mail.com', 'abcdef', 2))

# Insertion de quelques livres
cur.execute("INSERT INTO Books (titre, auteur, annee_publication, genre, isbn) VALUES (?, ?, ?, ?, ?)",
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1943, 'Conte', '978-2-07-040850-4'))
cur.execute("INSERT INTO Books (titre, auteur, annee_publication, genre, isbn) VALUES (?, ?, ?, ?, ?)",
            ('1984', 'George Orwell', 1949, 'Science-fiction', '978-0-452-28423-4'))
cur.execute("INSERT INTO Books (titre, auteur, annee_publication, genre, isbn) VALUES (?, ?, ?, ?, ?)",
            ('Les Misérables', 'Victor Hugo', 1862, 'Roman', '978-2-07-041234-2'))

# Insertion du stock des livres
cur.execute("INSERT INTO Stocks (livre_id, quantite, emplacement) VALUES (?, ?, ?)", (1, 5, 'Rayon 1A'))
cur.execute("INSERT INTO Stocks (livre_id, quantite, emplacement) VALUES (?, ?, ?)", (2, 3, 'Rayon 2B'))
cur.execute("INSERT INTO Stocks (livre_id, quantite, emplacement) VALUES (?, ?, ?)", (3, 2, 'Rayon 3C'))

# Validation des modifications et fermeture de la connexion
connection.commit()
connection.close()

print("Base de données créée et initialisée avec succès ! 🎉")
