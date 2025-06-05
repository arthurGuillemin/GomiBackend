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



#  Users    #

#GET
def get_user_by_id(user_id):
    """Récupérer un utilisateur spécifique par son ID"""
    try:
        response = supabase_client.table("Users").select("*").eq("id", user_id).single().execute()

        if not response.data:  
            return {"error": "Utilisateur non trouvé"}

        return response.data 

    except Exception as e:
        return {"error": str(e)}  
    


# POST

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
    """Vérifie les identifiants et retourne id username et email si ok"""
    response = supabase_client.table("Users").select("id, password , username , email").eq("email", email).execute()

    if not response.data or len(response.data) == 0:
        return {"error": "Email ou mot de passe incorrect"}
    user = response.data[0]
    if not check_password_hash(user['password'], password):
        return {"error": "Email ou mot de passe incorrect"}
    return {
        "user_id": user["id"],
        "email": user["email"],
        "username": user["username"]
    }

    
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


    