from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clé secrète pour la session

def create_connection():
    """ Créer une connexion à la base de données MySQL """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='db',
            user='root',
            password='password',
            database='test_db'
        )
        print("Connexion à la base de données réussie.")
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
    return connection

@app.route('/')
def formulaire():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    nom = request.form['nom']
    prenom = request.form['prenom']
    matricule = request.form['matricule']

    connection = create_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("INSERT INTO collaborateurs (nom, prenom, matricule) VALUES (%s, %s, %s)", (nom, prenom, matricule))
        connection.commit()
        message = "Collaborateur ajouté avec succès !"  # Message de succès
    except Error as e:
        print(f"Erreur lors de l'insertion dans la base de données : {e}")
        message = "Erreur lors de l'ajout du collaborateur."
    finally:
        cursor.close()
        connection.close()

    return render_template('success.html', message=message)  # Affiche une page de succès





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            session['user_id'] = user[0]  # Stocke l'ID de l'utilisateur dans la session
            return redirect(url_for('view_collaborateurs'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect", 401
            
    return render_template('login.html')


@app.route('/collaborateurs', methods=['GET', 'POST'])
def view_collaborateurs():
    # Vérifie si l'utilisateur est connecté
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirige vers la page de connexion si non authentifié

    connection = create_connection()
    cursor = connection.cursor()

    search_query = request.args.get('search')  # Récupère le paramètre de recherche

    try:
        if search_query:
            cursor.execute("SELECT id, nom, prenom, matricule FROM collaborateurs WHERE nom LIKE %s OR prenom LIKE %s", 
                           ('%' + search_query + '%', '%' + search_query + '%'))
        else:
            cursor.execute("SELECT id, nom, prenom, matricule FROM collaborateurs")  # Aucune recherche, récupère tous les collaborateurs

        collaborateurs = cursor.fetchall()
    except Error as e:
        print(f"Erreur lors de la récupération des collaborateurs : {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    return render_template('collaborateurs.html', collaborateurs=collaborateurs, search_query=search_query)



@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Supprime l'utilisateur de la session
    return '', 204  # Retourne un code de succès sans contenu

@app.route('/delete/<int:collaborateur_id>', methods=['POST'])
def delete_collaborateur(collaborateur_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("DELETE FROM collaborateurs WHERE id = %s", (collaborateur_id,))
        connection.commit()
        message = "Collaborateur supprimé avec succès !"  # Message de succès
    except Error as e:
        print(f"Erreur lors de la suppression du collaborateur : {e}")
        message = "Erreur lors de la suppression du collaborateur."
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('view_collaborateurs'))  # Redirige vers la liste des collaborateurs

@app.route('/edit/<int:collaborateur_id>', methods=['GET', 'POST'])
def edit_collaborateur(collaborateur_id):
    connection = create_connection()
    cursor = connection.cursor()

    # Vérifier si le collaborateur existe avant d'essayer de l'afficher
    cursor.execute("SELECT id, nom, prenom, matricule FROM collaborateurs WHERE id = %s", (collaborateur_id,))
    collaborateur = cursor.fetchone()

    if collaborateur is None:
        return "Collaborateur non trouvé", 404  # Gérer le cas où le collaborateur n'existe pas

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        matricule = request.form['matricule']
        
        try:
            cursor.execute("UPDATE collaborateurs SET nom = %s, prenom = %s, matricule = %s WHERE id = %s", 
                           (nom, prenom, matricule, collaborateur_id))
            connection.commit()
            return redirect(url_for('view_collaborateurs'))  # Redirection vers la liste des collaborateurs
        except Error as e:
            print(f"Erreur lors de la mise à jour du collaborateur : {e}")
            return jsonify({"error": str(e)}), 500

    cursor.close()
    connection.close()

    return render_template('edit_collaborateur.html', collaborateur=collaborateur)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
