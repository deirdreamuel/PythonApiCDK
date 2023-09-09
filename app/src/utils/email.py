import boto3


def send_email(sender: str, recipient: str, subject: str, body: str) -> None:
    ses_client = boto3.client("ses")

    ses_client.send_email(
        Source=sender,
        Destination={"ToAddresses": [recipient]},
        Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
    )
