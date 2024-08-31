from services.aws_email_service import AwsEmailService
from utils.constants import EmailServiceType
from interfaces.email_service_interface import IEmailService


class EmailServiceFactory:
    @staticmethod
    def get_service(service_type: EmailServiceType) -> IEmailService:
        if service_type == EmailServiceType.AWS_SES:
            return AwsEmailService()
        else:
            raise ValueError(f"Unknown service type: {service_type}")
