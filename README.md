# 🔐 Gomi - Backend (Authentification Flask + Supabase)

Ce backend gère l'authentification pour l'application **Gomi**
- la création de compte utilisateur,
- la connexion sécurisée,
- la génération de tokens JWT,
- la communication avec Supabase pour stocker les utilisateurs.

---


## 🚀 Lancement

### ⚙️ 1. Prérequis

- Python 3.9+ installé
- Un fichier `.env` à la racine du dossier `server` avec :

```env
SUPABASE_URL=...
SUPABASE_KEY=...
JWT_SECRET_KEY=...
FLASK_DEBUG=false
FLASK_ENV=development
```

---

### Option 1 : Lancer à la main

```bash
python -m venv .venv
source .venv/bin/activate  # (.venv\Scripts\activate sur Windows)
cd server
pip install -r requirements.txt
python run.py
```

Par défaut, le serveur démarre sur [http://localhost:5000](http://localhost:5000)

---

### 🐳 Option 2 : Lancer avec Docker Compose

Assurez-vous d’être dans le dossier racine du projet (`server/` ) contenant le `docker-compose.yml` :

```bash
docker compose up --build
```

Cela construira l’image Docker et démarrera automatiquement l’API Flask sur http://localhost

---

## 📁 Structure du dossier

```
server/
├── app/
│   ├── routes/              # routes
│   ├── schemas/             # schemas
│   └── services/            # fonctions supabases
│   └── tests/               # pytest
│   └── __init.py__/         # Flask factory

├── run.py                   # point d'entrée de l'app
├── requirements.txt
└── README.md                
```

---

## Auteur 

Arthur Guillemin