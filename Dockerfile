FROM python:3.9-slim

WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le fichier app.py dans le container
COPY app.py .

# Exposer le port 5000
EXPOSE 5000

# Commande à exécuter
CMD ["python", "app.py"]
