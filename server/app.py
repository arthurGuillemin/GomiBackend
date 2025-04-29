from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Import routes

from routes.test_routes import test_routes
from routes.user_routes import user_routes
from routes.auth_routes import auth_routes


# Register routes
app.register_blueprint(user_routes, url_prefix="/users")
app.register_blueprint(auth_routes, url_prefix="/auth")








app.register_blueprint(test_routes, url_prefix="/test")


if __name__ == '__main__':
    app.run(debug=True)
