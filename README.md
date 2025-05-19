#  Backend - Authentification Flask + Supabase

Ce backend Flask permet la gestion de l'authentification via Supabase avec création de compte, connexion et génération de jeton JWT pour l'app Gomi

## 🧾 Prérequis

- Python 3.9+
- pip (installé avec Python)

## 🚀 Installation

1. **Clonez ce dépôt**

```bash
git clone https://github.com/arthurGuillemin/BackendProvisional
cd BackendProvisional
```

2 . **Installez les dépendances **
```bash
pip install -r requirements.txt
```
3 . **Ajoutez vos variables d'environnemnt**
Créer un fichier .env avec :

```.env
SUPABASE_URL = ""
SUPABASE_KEY = ""
```

4 . **Lancez le serveur**
```bash
cd server
python app.py
```

🧑‍💻 Développé avec : 

Flask  ; Flask-JWT-Extended   ;Supabase Python client

