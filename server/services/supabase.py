import os
import jwt
from dotenv import load_dotenv
from supabase import create_client , Client
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

#   JWT #

def generate_token(user_id):
    """Génère un token JWT"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=2)
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
    """Teste la connexion à la db en recuperant tout les users    A SUPPRIMER !!!!!!!!"""
    try:
        response = supabase_client.table("Users").select("*").execute()
        return response.data 
    except Exception as e:
        return {"error": str(e)}
    