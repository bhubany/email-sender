from typing import List
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from email import encoders
from io import BytesIO
import logging
import os
from interfaces.email_service_interface import IEmailService
from aws.aws_config import AwsServices, AwsConfig
from utils.constants import EmailServiceType


logger = logging.getLogger(__name__)


class AwsEmailService(IEmailService):
    def __init__(self):
        self.ses_client = AwsConfig().get_client(AwsServices.SES)
        # self.config = TaxExemptAppConfig()

    def send_email(self, to: List[str], template_name: str, params=None, attachments=None):
        # tc = self.config.email.templates.get(template_name)
        # if not tc:
        #     raise RuntimeError(f"Unable to find template configuration for template {template_name}")

        # if self.config.email.email_suppressed or tc.email_suppressed:
        #     logger.error(f"Either system or {template_name} email is suppressed; not sending email.")
        #     return None

        if params is None:
            params = {}

        # body = self._parse_template_body(tc.template_path, params)
        # from_address = tc.from_address or self.config.email.from_address
        # reply_to = tc.reply_to_address or self.config.email.reply_to_address
        # subject = tc.subject.format(**params)

        return ""
        # if attachments:
        #     return self._send_via_ses_client_with_attachment(from_address, to, reply_to, subject, body, attachments, tc.cc_addresses, tc.bcc_addresses)
        # else:
        #     return self._send_via_ses_client(from_address, to, reply_to, subject, body, True, tc.cc_addresses, tc.bcc_addresses)

    def _send_via_ses_client(self, from_address, to, reply_to, subject, body, is_html, cc_address=None, bcc_address=None):
        destination = {
            'ToAddresses': to,
            'CcAddresses': cc_address or [],
            'BccAddresses': bcc_address or []
        }
        message = {
            'Subject': {'Data': subject},
            'Body': {'Html' if is_html else 'Text': {'Data': body}}
        }

        try:
            response = self.ses_client.send_email(
                FromEmailAddress=from_address,
                Destination=destination,
                ReplyToAddresses=[reply_to],
                Content={'Simple': message}
            )
            return response['MessageId']
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to send email: {e}")
            raise EmailException("Failed to send email") from e

    def _send_via_ses_client_with_attachment(self, from_address, to, reply_to, subject, body, attachments, cc_address=None, bcc_address=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = from_address
            msg['To'] = COMMASPACE.join(to)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            for attachment in attachments:
                part = MIMEApplication(attachment['data'])
                part.add_header('Content-Disposition',
                                'attachment', filename=attachment['name'])
                msg.attach(part)

            raw = msg.as_string().encode('utf-8')

            response = self.ses_client.send_email(
                Content={'Raw': {'Data': raw}},
                FromEmailAddress=from_address
            )

            return response['MessageId']
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to send email with attachment: {e}")
            raise Exception("Failed to send email with attachment") from e

    def _parse_template_body(self, template_path, params):
        with open(template_path, 'r') as template_file:
            template = template_file.read()
        return template.format(**params)
