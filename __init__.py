from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def accueil():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':  # À sécuriser
            session['authentifie'] = True
            return redirect(url_for('lecture'))
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

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


@app.route('/gestion_utilisateurs', methods=['GET', 'POST'])
def gestion_utilisateurs():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "Ajouter":
            nom = request.form['nom']
            email = request.form['email']
            mot_de_passe = request.form['mot_de_passe']
            role_id = request.form['role_id']
            cursor.execute("INSERT INTO Users (nom, email, mot_de_passe, role_id) VALUES (?, ?, ?, ?)", 
                           (nom, email, mot_de_passe, role_id))
            conn.commit()

        elif action == "Supprimer":
            user_id = request.form['user_id']
            cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
            conn.commit()

        elif action == "Modifier":
            user_id = request.form['user_id']
            nom = request.form['nom']
            email = request.form['email']
            role_id = request.form['role_id']
            cursor.execute("UPDATE Users SET nom = ?, email = ?, role_id = ? WHERE id = ?", 
                           (nom, email, role_id, user_id))
            conn.commit()

    cursor.execute("SELECT Users.id, Users.nom, Users.email, Roles.nom_role FROM Users JOIN Roles ON Users.role_id = Roles.id")
    users = cursor.fetchall()
    conn.close()

    return render_template('gestion_utilisateurs.html', users=users)


if __name__ == "__main__":
    app.run(debug=True)
