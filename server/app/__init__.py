from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_talisman import Talisman
from flasgger import Swagger

import os
load_dotenv()

from .config import Config

from app.routes.auth_routes import auth_routes
from app.routes.user_routes import user_routes
from app.routes.swagger_redirect_routes import swagger_redirect_routes


jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Swaggr
    template = {
    "swagger": "2.0",
    "info": {
        "title": "Gomi API",
        "description": "API pour gerer les utilisateurs et l'authentification",
        "contact": {
            "name": "Arthur Guillemin",
            "url": "https://github.com/arthurGuillemin",
            "email": "aguillemin291@gmail.com",
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "host": "https://flask-backend-gomi-hbbjbyc9agend4fh.francecentral-01.azurewebsites.net/",  
    "basePath": "/",
    "schemes": ["https", "http"]
}

    swagger = Swagger(app , template=template)
    

    # Extensions
    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
    jwt.init_app(app)
    limiter.init_app(app)

    # Routes
    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(user_routes, url_prefix="/users")
    app.register_blueprint(swagger_redirect_routes)

    
    #talisman
    is_prod = os.getenv("FLASK_ENV") == "production"
    Talisman(app, content_security_policy=None , force_https=is_prod) 


    return app
