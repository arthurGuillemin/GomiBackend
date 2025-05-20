from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.supabase import create_user, login_user

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/signup", methods=["POST"])
def signup():
    """ Créer un compte"""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Username, email et mot de passe requis pour l'inscription"}), 400
    result = create_user(username, email, password)
    return jsonify(result), 201

@auth_routes.route("/login", methods=["POST"])
def login():
    """Connecter un utilisateur"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis opur la conneciton"}), 400

    result = login_user(email, password)

    if "error" in result:
        return jsonify(result), 401

    token = create_access_token(identity=result["user_id"] , expires_delta= False)
    return jsonify({
        "message": "Connexion réussie",
        "token": token,
        "user_id": result["user_id"]
    }), 200
