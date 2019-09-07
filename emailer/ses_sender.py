import logging
import boto3
from botocore.exceptions import ClientError
from .base import Sender

logger = logging.getLogger(__name__)


class SESSender(Sender):
    def __init__(self, address, aws_region="us-east-1", charset="utf-8"):
        super().__init__(address)
        self.aws_region = aws_region
        self.charset = charset

    def __call__(self, email, subject, html, text):
        logger.debug(
            f"AWS SES attempting to send email to {email} from AWS region "
            f"{self.aws_region} with sender {self.address}; charset {self.charset}"
        )
        try:
            response = boto3.client("ses", region_name=self.aws_region).send_email(
                Destination={"ToAddresses": [email]},
                Message={
                    "Body": {
                        "Html": {"Charset": self.charset, "Data": html},
                        "Text": {"Charset": self.charset, "Data": text},
                    },
                    "Subject": {"Charset": self.charset, "Data": subject},
                },
                Source=self.address,
            )
        except ClientError:
            logger.error(f"Unable to send email to {email} via AWS SES", exc_info=True)
            raise
        else:
            message = f"Sent email to {email}; subject '{subject}' via AWS SES"

            if logger.level > logging.DEBUG:
                logger.info(f"{message}; Message ID is {response['MessageId']}")
            else:
                logger.debug(f"{message}; response is {response}")
