from flask import Flask
from flask_cors import CORS


# routes

from routes.test_routes import test_routes


app = Flask(__name__)
CORS(app)




app.register_blueprint(test_routes, url_prefix="/test")


if __name__ == '__main__':
    app.run(debug=True)
