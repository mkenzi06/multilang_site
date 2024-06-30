# djangomultlingue
Ce projet est une application Django multilingue utilisant une base de données SQLite. Il est conçu pour être déployé sur AlwaysData.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine locale :

- Python 3.x
- Pip (gestionnaire de paquets pour Python)
- Git

## Installation et Configuration Locale

1. **Clonez le dépôt**

   ```bash
   git clone https://github.com/votre_utilisateur/multilingue_site.git
   cd multilingue_site
2. **creer environnement virtuelle**   
python -m venv env
3. **generer le fichier des dependances**
pip install -r requirements.txt
4. **migrer la BD (sqlite)**
python manage.py migrate
5. **lancer le serveur**
python manage.py runserver
6. **rajouter cette ligne dans procfile**
web: gunicorn multilang_site.wsgi


## deploiement sur render
Connecter Render à votre dépôt GitHub

Allez sur Render.
Connectez-vous ou créez un compte.
Cliquez sur "New" puis "Web Service".
Connectez votre compte GitHub et autorisez Render à accéder à vos dépôts.
Sélectionnez votre dépôt multilingue.
Configurer le déploiement

Nom : Donnez un nom à votre service.
Branch : Sélectionnez main.
Build Command : Laissez vide ou mettez pip install -r requirements.txt.
Start Command : gunicorn multilang_site.wsgi:application.
Environment : Sélectionnez Python 3.
Region : Choisissez votre région préférée.
Ajouter des variables d'environnement

Cliquez sur "Add Environment Variable".
Ajoutez la variable DJANGO_SETTINGS_MODULE avec la valeur multilang_site.settings.
Ajoutez toute autre variable d'environnement nécessaire.
Lancer le déploiement

Cliquez sur "Create Web Service" pour démarrer le déploiement. Render va maintenant construire et déployer votre application.
