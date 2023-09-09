import unittest
from unittest.mock import patch

from flask import Flask

from botocore.exceptions import ClientError
from requests.exceptions import RequestException


from src.routes.notifications import routes


class NotificationsRoutesTestSuite(unittest.TestCase):
    @patch("src.routes.notifications.requests")
    def test_when_success_return_200(self, requests_mock):
        with patch("src.routes.notifications.send_email") as send_email_mock:
            requests_mock.get.return_value.status_code = 200
            requests_mock.get.return_value.json.return_value = (
                self.get_successful_api_response()
            )

            send_email_mock.return_value = None

            app = Flask(__name__)
            app.testing = True
            app.register_blueprint(routes)

            response = app.test_client().post("/daily-notifications")
            assert response.status_code == 200

    @patch("src.routes.notifications.requests")
    def test_when_requests_exception_return_500(self, requests_mock):
        with patch("src.routes.notifications.send_email") as send_email_mock:
            requests_mock.get.side_effect = RequestException("RequestError")

            send_email_mock.return_value = None

            app = Flask(__name__)
            app.testing = True
            app.register_blueprint(routes)

            response = app.test_client().post("/daily-notifications")
            assert response.status_code == 500

    @patch("src.routes.notifications.requests")
    def test_when_send_email_exception_return_500(self, requests_mock):
        with patch("src.routes.notifications.send_email") as send_email_mock:
            requests_mock.get.return_value.status_code = 200
            requests_mock.get.return_value.json.return_value = (
                self.get_successful_api_response()
            )

            send_email_mock.side_effect = ClientError(
                {"Error": {"Code": 500, "Message": "Error"}}, "send_email"
            )

            app = Flask(__name__)
            app.testing = True
            app.register_blueprint(routes)

            response = app.test_client().post("/daily-notifications")
            assert response.status_code == 500

    def get_successful_api_response(self) -> dict:
        return {
            "afterHours": 192.45,
            "close": 192.46,
            "from": "2023-07-03",
            "high": 193.88,
            "low": 191.76,
            "open": 193.78,
            "preMarket": 193.99,
            "status": "OK",
            "symbol": "AAPL",
            "volume": 31458198.0,
        }
