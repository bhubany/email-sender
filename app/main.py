import boto3
import json
from lib.aws_config import AwsConfiguration, AwsServices

aws_s3_service = AwsConfiguration().get_client(service=AwsServices.S3)
print(aws_s3_service.Object(bucket_name=''))
