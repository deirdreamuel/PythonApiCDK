import json
import unittest
from unittest.mock import patch

from flask import Flask

from boto3.dynamodb.conditions import Key


from src.routes.subscriptions import (
    post_stock_subscriptions,
    routes,
    get_stock_subscriptions,
)


class SubscriptionsRoutesTestSuite(unittest.TestCase):
    @patch("src.routes.subscriptions.get_stock_subscriptions")
    def test_when_get_subscriptions_success_return_200(self, get_subscriptions_mock):
        get_subscriptions_mock.return_value = []

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().get(
            "/subscriptions", query_string={"uid": "example@test.com"}
        )
        assert response.status_code == 200

    @patch("src.routes.subscriptions.get_stock_subscriptions")
    def test_when_get_subscriptions_params_null_return_400(
        self, get_subscriptions_mock
    ):
        get_subscriptions_mock.return_value = []

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().get("/subscriptions")
        assert response.status_code == 400

    @patch("src.routes.subscriptions.get_stock_subscriptions")
    def test_when_get_subscriptions_db_error_return_500(self, get_subscriptions_mock):
        get_subscriptions_mock.side_effect = Exception("DatabaseError")

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().get(
            "/subscriptions", query_string={"uid": "example@test.com"}
        )
        assert response.status_code == 500

    @patch("src.routes.subscriptions.post_stock_subscriptions")
    def test_when_post_subscriptions_success_return_200(self, post_subscriptions_mock):
        post_subscriptions_mock.return_value = None

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().post(
            "/subscriptions",
            data=json.dumps({"uid": "example@test.com", "stock": "AMZN"}),
            content_type="application/json",
        )
        assert response.status_code == 200

    @patch("src.routes.subscriptions.post_stock_subscriptions")
    def test_when_post_subscriptions_db_error_return_500(self, post_subscriptions_mock):
        post_subscriptions_mock.side_effect = Exception("DatabaseError")

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().post(
            "/subscriptions",
            data=json.dumps({"uid": "example@test.com", "stock": "AMZN"}),
            content_type="application/json",
        )
        assert response.status_code == 500

    @patch("src.routes.subscriptions.post_stock_subscriptions")
    def test_when_post_subscriptions_uid_null_return_400(self, post_subscriptions_mock):
        post_subscriptions_mock.return_value = None

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().post(
            "/subscriptions",
            data=json.dumps({"stock": "AMZN"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    @patch("src.routes.subscriptions.post_stock_subscriptions")
    def test_when_post_subscriptions_stock_null_return_400(
        self, post_subscriptions_mock
    ):
        post_subscriptions_mock.return_value = None

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().post(
            "/subscriptions",
            data=json.dumps({"uid": "example@test.com"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    @patch("src.routes.subscriptions.post_stock_subscriptions")
    def test_when_post_subscriptions_uid_empty_return_400(
        self, post_subscriptions_mock
    ):
        post_subscriptions_mock.return_value = None

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().post(
            "/subscriptions",
            data=json.dumps({"uid": "example@test.com", "stock": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400

    @patch("src.routes.subscriptions.post_stock_subscriptions")
    def test_when_post_subscriptions_stock_empty_return_400(
        self, post_subscriptions_mock
    ):
        post_subscriptions_mock.return_value = None

        app = Flask(__name__)
        app.testing = True
        app.register_blueprint(routes)

        response = app.test_client().post(
            "/subscriptions",
            data=json.dumps({"uid": "example@test.com", "stock": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400

    @patch("src.routes.notifications.dynamodb.Table")
    def test_when_get_stock_subscriptions_empty_db_success_return_empty_list(
        self, dynamodb_table_mock
    ):
        dynamodb_table_mock.return_value.query.return_value = {"Items": []}

        subscriptions = get_stock_subscriptions("example@test.com")

        dynamodb_table_mock.assert_called_once_with("SUBSCRIPTIONS")
        dynamodb_table_mock.return_value.query.assert_called_once_with(
            KeyConditionExpression=Key("PK").eq("USER#example@test.com")
            & Key("SK").begins_with("STOCK#")
        )

        self.assertListEqual(subscriptions, [])

    @patch("src.routes.notifications.dynamodb.Table")
    def test_when_get_stock_subscriptions_db_error_throw_exception(
        self, dynamodb_table_mock
    ):
        dynamodb_table_mock.return_value.query.side_effect = Exception("DatabaseError")

        with self.assertRaises(Exception) as context:
            get_stock_subscriptions("example@test.com")

        dynamodb_table_mock.assert_called_once_with("SUBSCRIPTIONS")
        dynamodb_table_mock.return_value.query.assert_called_once_with(
            KeyConditionExpression=Key("PK").eq("USER#example@test.com")
            & Key("SK").begins_with("STOCK#")
        )

        self.assertEqual(str(context.exception), "DatabaseError")

    @patch("src.routes.notifications.dynamodb.Table")
    def test_when_post_stock_subscriptions_success_return_none(
        self, dynamodb_table_mock
    ):
        dynamodb_table_mock.return_value.put_item.return_value = {"Items": []}

        post_stock_subscriptions("example@test.com", "AMZN")

        dynamodb_table_mock.assert_called_once_with("SUBSCRIPTIONS")
        dynamodb_table_mock.return_value.put_item.assert_called_once_with(
            Item={"PK": "USER#example@test.com", "SK": f"STOCK#AMZN", "stock": "AMZN"}
        )

    @patch("src.routes.notifications.dynamodb.Table")
    def test_when_post_stock_subscriptions_db_error_throw_exception(
        self, dynamodb_table_mock
    ):
        dynamodb_table_mock.return_value.put_item.side_effect = Exception(
            "DatabaseError"
        )

        with self.assertRaises(Exception) as context:
            post_stock_subscriptions("example@test.com", "AMZN")

        dynamodb_table_mock.assert_called_once_with("SUBSCRIPTIONS")
        dynamodb_table_mock.return_value.put_item.assert_called_once_with(
            Item={"PK": "USER#example@test.com", "SK": f"STOCK#AMZN", "stock": "AMZN"}
        )

        self.assertEqual(str(context.exception), "DatabaseError")
