import os
import jwt
from dotenv import load_dotenv
from supabase import create_client
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)


#       test       #

def test_db_connection():
    """Teste la connexion à la db en recuperant tout les Users    A SUPPRIMER !!!!!!!!"""
    try:
        response = supabase_client.table("Users").select("*").execute()
        return response.data 
    except Exception as e:
        return {"error": str(e)}
    

#  Users    #



# GET

def create_user(username, email, password):
    """Créer un nouvel utilisateur dans la base de données"""
    hashed_password = generate_password_hash(password)  

    response = supabase_client.table("Users").insert({
        "username": username,  
        "email": email,
        "password": hashed_password  
    }).execute()    
    return {"message": "Utilisateur créé avec succès"}

def login_user(email, password):
    """Vérifie les identifiants et retourne uniquement l'ID utilisateur si ok"""
    response = supabase_client.table("Users").select("id, password").eq("email", email).execute()

    if not response.data or len(response.data) == 0:
        return {"error": "Email ou mot de passe incorrect"}
    user = response.data[0]
    if not check_password_hash(user['password'], password):
        return {"error": "Email ou mot de passe incorrect"}
    return {
        "user_id": user["id"]
    }

def get_user_by_id(user_id):
    """Récupérer un utilisateur spécifique par son ID"""
    try:
        response = supabase_client.table("Users").select("*").eq("id", user_id).single().execute()

        if not response.data:  
            return {"error": "Utilisateur non trouvé"}

        return response.data 

    except Exception as e:
        return {"error": str(e)}  
    

def get_username_by_id(user_id):
    """Récupérer uniquement le username d'un utilisateur par son ID"""
    try:
        response = supabase_client.table("Users").select("username").eq("id", user_id).single().execute()

        if not response.data: 
            return {"error": "Utilisateur non trouvé"}

        return {"username": response.data["username"]} 

    except Exception as e:
        return {"error": str(e)} 
    
# Update

def update_user(user_id, updated_data):
    """Modifier les informations d'un utilisateur"""
    try:
        response = supabase_client.table("Users") \
            .update(updated_data) \
            .eq("id", user_id) \
            .execute()

        if response.data:
            return {"message": "Utilisateur mis à jour avec succès", "user": response.data}

        return {"error": "Aucune modification effectuée ou utilisateur introuvable"}

    except Exception as e:
        return {"error": str(e)}



# DELETE 

def delete_user(user_id):
    """Supprimer un utilisateur"""
    try:
        response = supabase_client.table("Users") \
            .delete() \
            .eq("id", user_id) \
            .execute()

        if response.data:
            return {"message": "Utilisateur supprimé avec succès"}

        return {"error": "Utilisateur introuvable ou déjà supprimé"}

    except Exception as e:
        return {"error": str(e)}


    