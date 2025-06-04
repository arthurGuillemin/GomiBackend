from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.supabase import create_user, login_user
from marshmallow import ValidationError
from app.schemas.auth_schemas import SignupSchema, LoginSchema

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/signup", methods=["POST"])
def signup():
    """
    Créer un compte
    ---
    tags:
      - Auth
    parameters:
      - name: username
        in: path
        required: true
        schema:
          type: string
        description: user's username
      - name: email
        in: path
        required: true
        schema:
          type: string
        description: email for user account
      - name: password
        in: path
        required: true
        schema:
          type: string
        description: account password
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - email
              - password
            properties:
              username:
                type: string
              email:
                type: string
              password:
                type: string
    responses:
      201:
        description: Compte créé avec succès
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                user_id:
                  type: string
      400:
        description: Données manquantes ou invalides
    """
    try:
        data = SignupSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    result = create_user(data["username"], data["email"], data["password"])
    return jsonify(result), 201

@auth_routes.route("/login", methods=["POST"])
def login():
    """
    Connecter un utilisateur
    ---
    tags:
      - Auth
    parameters:
      - name: email
        in: path
        required: true
        schema:
          type: string
        description: user email
      - name: password
        in: path
        required: true
        schema:
          type: string
        description: user password
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - email
              - password
            properties:
              email:
                type: string
              password:
                type: string
    responses:
      200:
        description: Connexion réussie
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                token:
                  type: string
                user_id:
                  type: string
                email:
                  type: string
                username:
                  type: string
      400:
        description: Email ou mot de passe manquant
      401:
        description: Identifiants invalides
    """
    try:
        data = LoginSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    result = login_user(data["email"], data["password"])
    if "error" in result:
        return jsonify(result), 401
    token = create_access_token(identity=result["user_id"], expires_delta=False)
    return jsonify({
        "message": "Connexion réussie",
        "token": token,
        "user_id": result["user_id"],
        "email": result["email"],
        "username": result["username"]
    }), 200
