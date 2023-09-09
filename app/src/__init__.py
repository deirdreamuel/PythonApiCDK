import os, logging
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
import serverless_wsgi

print(os.environ)

from src.routes import register_blueprints

app = Flask(__name__)
register_blueprints(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(message)s",
)


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
