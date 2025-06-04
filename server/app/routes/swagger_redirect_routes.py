from flask import Blueprint, redirect

swagger_redirect_routes = Blueprint("swagger_redirect_routes", __name__)

@swagger_redirect_routes.route("/", defaults={"path": ""})
@swagger_redirect_routes.route("/<path:path>")
def redirect_to_swagger(path):
    return redirect("/apidocs")
