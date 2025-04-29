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

#   JWT  #

def generate_token(user_id):
    """Génère un token JWT"""
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    """Décode un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


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
    """Vérifier les informations d'identification et retourner un token JWT + user_id"""
    response = supabase_client.table("Users").select("id, password").eq("email", email).execute()
    
    if not response.data or len(response.data) == 0:
        return {"error": "Email ou mot de passe incorrect"}
    
    user = response.data[0]
    if not check_password_hash(user['password'], password):
        return {"error": "Email ou mot de passe incorrect"}
    
    token = generate_token(user['id'])
    return {
        "message": "Connexion réussie",
        "token": token,
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

        return {"usernale": response.data["username"]} 

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


    