CREATE TABLE IF NOT EXISTS collaborateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    matricule VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Ajoute un utilisateur admin par défaut
INSERT INTO users (username, password) VALUES ('admin', 'admin123'); -- Mot de passe simple pour test

