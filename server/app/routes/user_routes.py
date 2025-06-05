from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.supabase import get_user_by_id, update_user, delete_user

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/<string:user_id>', methods=['GET'])
@jwt_required()
def getUserById(user_id):
    """
    Obtenir un utilisateur par son ID
    ---
    tags:
      - Users [jwt_required]
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: string
        description: ID de l'utilisateur à récupérer
    responses:
      200:
        description: Détails de l'utilisateur récupéré
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                username:
                  type: string
                email:
                  type: string
      401:
        description: Authentification requise / token invalide
    """
    result = get_user_by_id(user_id)
    return jsonify(result)


@user_routes.route('/<string:user_id>', methods=['DELETE'])
@jwt_required()
def deleteUser(user_id):
    """
    Supprimer un utilisateur par son ID
    ---
    tags:
      - Users [jwt_required]
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: string
        description: ID de l'utilisateur à supprimer
    responses:
      200:
        description: Utilisateur supprimé avec succès
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      401:
        description: Authentification requise / token invalide
      404:
        description: Utilisateur non trouvé ou déjà supprimé
    """
    result = delete_user(user_id)
    return jsonify(result)


@user_routes.route('/<string:user_id>', methods=['PUT'])
@jwt_required()
def updateUser(user_id):
    """
    Mettre à jour un utilisateur par son ID
    ---
    tags:
      - Users [jwt_required]
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: string
        description: ID de l'utilisateur à mettre à jour
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              email:
                type: string
    responses:
      200:
        description: Utilisateur mis à jour avec succès
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                user:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      username:
                        type: string
                      email:
                        type: string
      400:
        description: Aucune donnée fournie ou données invalides
      401:
        description: Authentification requise / token invalide
      404:
        description: Utilisateur non trouvé
    """
    data = request.json
    if not data:
        return jsonify({"error": "Aucune donnée fournie"}), 400
    result = update_user(user_id, data)
    return jsonify(result)
