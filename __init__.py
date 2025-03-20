from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

@app.route('/stock', methods=['GET', 'POST'])
def afficher_stock():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "Ajouter":
            try:
                titre = request.form['titre']
                auteur = request.form['auteur']
                annee_publication = request.form['annee_publication']
                genre = request.form['genre']
                isbn = request.form['isbn']
                quantite = request.form['quantite']
                emplacement = request.form['emplacement']

                print(f"📌 Ajout du livre : {titre} | {auteur} | {annee_publication} | {genre} | {isbn} | {quantite} | {emplacement}")

                # Vérifier si le livre existe déjà (par ISBN)
                cursor.execute("SELECT id FROM Books WHERE isbn = ?", (isbn,))
                existing_book = cursor.fetchone()

                if existing_book:
                    livre_id = existing_book[0]
                    print("🔄 Livre déjà existant, mise à jour du stock...")
                else:
                    # Ajouter le livre dans la table Books
                    cursor.execute("INSERT INTO Books (titre, auteur, annee_publication, genre, isbn) VALUES (?, ?, ?, ?, ?)",
                                   (titre, auteur, annee_publication, genre, isbn))
                    livre_id = cursor.lastrowid
                    print(f"✅ Livre ajouté avec ID {livre_id}")

                # Ajouter ou mettre à jour le stock
                cursor.execute("SELECT id FROM Stocks WHERE livre_id = ?", (livre_id,))
                existing_stock = cursor.fetchone()

                if existing_stock:
                    cursor.execute("UPDATE Stocks SET quantite = quantite + ? WHERE livre_id = ?", (quantite, livre_id))
                    print("🔄 Stock mis à jour")
                else:
                    cursor.execute("INSERT INTO Stocks (livre_id, quantite, emplacement) VALUES (?, ?, ?)",
                                   (livre_id, quantite, emplacement))
                    print("✅ Stock ajouté")

                conn.commit()
                flash("📚 Livre ajouté ou mis à jour dans le stock !", "success")

            except Exception as e:
                print(f"⚠️ ERREUR : {e}")
                flash(f"Erreur lors de l'ajout : {e}", "danger")

        elif action == "Supprimer":
            try:
                livre_id = request.form['livre_id']
                cursor.execute("DELETE FROM Stocks WHERE livre_id = ?", (livre_id,))
                cursor.execute("DELETE FROM Books WHERE id = ?", (livre_id,))
                conn.commit()
                flash("❌ Livre supprimé avec succès !", "danger")
            except Exception as e:
                print(f"⚠️ ERREUR lors de la suppression : {e}")
                flash(f"Erreur lors de la suppression : {e}", "danger")

    # Récupérer la liste des livres avec leurs stocks
    cursor.execute('''
        SELECT Books.id, Books.titre, Books.auteur, Books.annee_publication, Books.genre, Books.isbn,
               Stocks.quantite, Stocks.emplacement
        FROM Books
        JOIN Stocks ON Books.id = Stocks.livre_id
        ORDER BY Books.titre ASC;
    ''')
    stock_data = cursor.fetchall()
    conn.close()

    return render_template('stock.html', stock=stock_data)




@app.route('/test')
def test():
    return "Flask fonctionne correctement !"

@app.route('/')
def accueil():
    return render_template('accueil.html')




@app.route('/gestion_utilisateurs', methods=['GET', 'POST'])
def gestion_utilisateurs():
    print("➡️ Route /gestion_utilisateurs appelée")  # Debug

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')
        print(f"📌 Action reçue : {action}")  # Debug

        try:
            if action == "Ajouter":
                nom = request.form['nom']
                email = request.form['email']
                mot_de_passe = request.form['mot_de_passe']
                role_id = request.form['role_id']
                print(f"✅ Ajout de l'utilisateur : {nom}, {email}, {role_id}")  # Debug
                
                cursor.execute("INSERT INTO Users (nom, email, mot_de_passe, role_id) VALUES (?, ?, ?, ?)", 
                               (nom, email, mot_de_passe, role_id))
                conn.commit()

            elif action == "Supprimer":
                user_id = request.form['user_id']
                print(f"❌ Suppression de l'utilisateur ID : {user_id}")  # Debug
                
                cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
                conn.commit()

            elif action == "Modifier":
                user_id = request.form['user_id']
                nom = request.form['nom']
                email = request.form['email']
                role_id = request.form['role_id']
                print(f"✏️ Modification de l'utilisateur ID : {user_id}")  # Debug

                cursor.execute("UPDATE Users SET nom = ?, email = ?, role_id = ? WHERE id = ?", 
                               (nom, email, role_id, user_id))
                conn.commit()

        except sqlite3.Error as e:
            print(f"⚠️ Erreur SQLite : {e}")  # Debug
            conn.rollback()

    # Récupération des utilisateurs
    cursor.execute("SELECT Users.id, Users.nom, Users.email, Roles.nom_role FROM Users JOIN Roles ON Users.role_id = Roles.id")
    users = cursor.fetchall()
    print(f"📌 Utilisateurs récupérés : {users}")  # Debug

    conn.close()
    return render_template('gestion_utilisateurs.html', users=users)



if __name__ == "__main__":
    app.run(debug=True)
