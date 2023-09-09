import unittest
from unittest.mock import patch

from src.utils.email import send_email


class EmailUtilTests(unittest.TestCase):
    @patch("src.utils.email.boto3.client")
    def test_when_send_email_success_return_none(self, mock_client):
        mock_send_email = mock_client.return_value.send_email
        mock_send_email.return_value = {"MessageId": "test_message_id"}

        sender = "sender@example.com"
        recipient = "recipient@example.com"
        subject = "Test Email"
        body = "This is a test email."

        send_email(sender, recipient, subject, body)

        mock_client.assert_called_once_with("ses")
        mock_send_email.assert_called_once_with(
            Source=sender,
            Destination={"ToAddresses": [recipient]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )

    @patch("src.utils.email.boto3.client")
    def test_when_send_email_error_throw_exception(self, mock_client):
        mock_send_email = mock_client.return_value.send_email
        mock_send_email.side_effect = Exception("ClientError")

        sender = "sender@example.com"
        recipient = "recipient@example.com"
        subject = "Test Email"
        body = "This is a test email."

        with self.assertRaises(Exception) as context:
            send_email(sender, recipient, subject, body)

        mock_client.assert_called_once_with("ses")
        mock_send_email.assert_called_once_with(
            Source=sender,
            Destination={"ToAddresses": [recipient]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )

        self.assertEqual(str(context.exception), "ClientError")


if __name__ == "__main__":
    unittest.main()
