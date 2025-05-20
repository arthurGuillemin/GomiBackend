from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_talisman import Talisman

import os
load_dotenv()

from .config import Config

from app.routes.auth_routes import auth_routes
from app.routes.user_routes import user_routes
from app.routes.test_routes import test_routes


jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
    jwt.init_app(app)
    limiter.init_app(app)

    # Routes
    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(user_routes, url_prefix="/users")
    app.register_blueprint(test_routes, url_prefix="/test")

    #talisman
    is_prod = os.getenv("FLASK_ENV") == "production"
    Talisman(app, content_security_policy=None , force_https=is_prod) 


    return app
