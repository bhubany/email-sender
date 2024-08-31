from factories.email_service_factory import EmailServiceFactory
from utils.constants import EmailServiceType


def main():
    service = EmailServiceFactory().get_service(EmailServiceType.AWS_SES)
    service.send_email(to=["bhuban.smaitic@gmail.com"],
                       template_name="welcome-email", attachments=None)


if __name__ == "__main__":
    main()
