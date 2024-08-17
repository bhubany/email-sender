import boto3
import os
from enum import Enum
from utils.env_utils import get_environment_variable_or_default


class AwsServices(Enum):
    S3 = 's3'
    SES = 'ses'


class AwsConfiguration:
    def __init__(self):
        self.__region = get_environment_variable_or_default(
            'AWS_REGION', "ap-south-1")
        self.__session = boto3.Session(
            aws_access_key_id=get_environment_variable_or_default(
                'AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=get_environment_variable_or_default(
                'AWS_SECRET_ACCESS_KEY'),
            aws_session_token=get_environment_variable_or_default(
                'AWS_SESSION_TOKEN'),
        )

    def region(self) -> str:
        return self.__region

    def get_client(self, service: AwsServices) -> boto3.client:
        return self.__session.client(service_name=service.value, region_name=self.__region)
