from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
import serverless_wsgi

from src.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
