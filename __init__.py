from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions



# Nouvelle route pour afficher le stock des livres
@app.route('/stock')
def afficher_stock():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécuter la requête SQL pour récupérer les stocks de livres
    cursor.execute('''
        SELECT Books.id, Books.titre, Books.auteur, Stocks.quantite, Stocks.emplacement
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
