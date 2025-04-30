from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    get_remote_address, 
    app=app,
    default_limits=["10 per minute"],
)

# Import routes

from routes.test_routes import test_routes
from routes.user_routes import user_routes
from routes.auth_routes import auth_routes


# Register routes
app.register_blueprint(user_routes, url_prefix="/users")
app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(test_routes, url_prefix="/test")


app.run(host="0.0.0.0", port=5000, debug=True)

