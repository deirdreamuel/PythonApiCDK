from flask import jsonify, Blueprint, request

import logging

from src.lib.db import dynamodb

from boto3.dynamodb.conditions import Key
from http import HTTPStatus as status

from src.models import subscription, validator

routes = Blueprint("subscriptions", __name__)


@routes.route("/subscriptions", methods=["GET"])
def get_subscriptions_handler():
    try:
        uid = request.args.get("uid")

        if not uid:
            return (
                jsonify({"message": "'uid' query parameter is missing or empty"}),
                status.BAD_REQUEST,
            )

        subscriptions = get_stock_subscriptions(uid)

        return jsonify(subscriptions)

    except Exception as error:
        logging.error(error)
        return (
            jsonify({"message": "Internal Server Error"}),
            status.INTERNAL_SERVER_ERROR,
        )


@routes.route("/subscriptions", methods=["POST"])
def post_subscriptions_handler():
    try:
        data = request.get_json()

        valid = validator.validate(data, subscription.schema)
        if not valid:
            return {"errors": validator.errors}, status.BAD_REQUEST

        post_stock_subscriptions(data["uid"], data["stock"])
        return jsonify({"message": "success"}), 200

    except Exception as error:
        logging.error(error)
        return (
            jsonify({"message": "Internal Server Error"}),
            status.INTERNAL_SERVER_ERROR,
        )


def get_stock_subscriptions(uid: str) -> list[dict]:
    result = dynamodb.Table("SUBSCRIPTIONS").query(
        KeyConditionExpression=Key("PK").eq(f"USER#{uid}")
        & Key("SK").begins_with("STOCK#")
    )

    return result["Items"]


def post_stock_subscriptions(uid: str, stock: str) -> None:
    item = {"PK": f"USER#{uid}", "SK": f"STOCK#{stock}", "stock": stock}

    dynamodb.Table("SUBSCRIPTIONS").put_item(Item=item)
