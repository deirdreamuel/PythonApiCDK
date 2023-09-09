from datetime import date, timedelta
from flask import jsonify, Blueprint, request

import os, requests, logging

from requests.exceptions import RequestException
from botocore.exceptions import ClientError

from src.lib.db import dynamodb
from src.routes.subscriptions import get_stock_subscriptions
from src.utils.email import send_email

from boto3.dynamodb.conditions import Key
from http import HTTPStatus as status

from src.utils.is_weekday import is_weekday


routes = Blueprint("notifications", __name__)

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")


@routes.route("/daily-notifications", methods=["POST"])
def daily_notifications_handler():
    try:
        yesterday = date.today() - timedelta(days=1)

        stocks_info_list: list[dict] = []

        subscriptions = get_stock_subscriptions(uid="deirdreamuel@gmail.com")
        for subscription in subscriptions:
            response = requests.get(
                url=f"https://api.polygon.io/v1/open-close/{subscription['stock']}/{yesterday.strftime('%Y-%m-%d')}",
                params={"adjusted": "true"},
                headers={"Authorization": f"Bearer {POLYGON_API_KEY}"},
            )

            stocks_info_list.append(response.json())

        if len(subscriptions) > 0 and is_weekday(yesterday):
            print('sending email...')
            send_email(
                "no-reply@amuel.org",
                "deirdreamuel@gmail.com",
                "Test Email Subject",
                str(stocks_info_list),
            )

        return jsonify(stocks_info_list)

    except (RequestException, ClientError) as error:
        logging.error(error)
        return (
            jsonify({"message": "Internal Server Error"}),
            status.INTERNAL_SERVER_ERROR,
        )
