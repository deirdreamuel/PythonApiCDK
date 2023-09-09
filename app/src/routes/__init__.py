from flask import Blueprint, jsonify

from src.routes import notifications, subscriptions

routes = Blueprint("", __name__)


@routes.route("/hello", methods=["POST"])
def hello_world():
    return jsonify({"message": "hello_world"})


# Function to register all the blueprints
def register_blueprints(app):
    app.register_blueprint(routes)
    app.register_blueprint(notifications.routes)
    app.register_blueprint(subscriptions.routes)
