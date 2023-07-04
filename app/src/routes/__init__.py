from datetime import date, timedelta
from flask import Blueprint, jsonify
import requests

routes = Blueprint("", __name__)


@routes.route("/hello", methods=["POST"])
def hello_world():
    return jsonify({"message": "hello_world"})
