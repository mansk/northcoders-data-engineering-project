import boto3
from botocore.exceptions import ClientError
# from hashlib import sha256
try:
    from utils.custom_exceptions import *
except ModuleNotFoundError:
    from src.custom_exceptions import *


client = boto3.client('s3')


def write_object_to_s3_bucket(bucket_name, file_key, data):
    try:
        response = client.put_object(
            Body=data.encode('utf_8'),
            Bucket=bucket_name,
            # ChecksumSHA256 = sha256(bytes(data, encoding='utf_8')),
            Key=file_key)

        if ('ResponseMetadata' in response and
            'HTTPStatusCode' in response['ResponseMetadata'] and
            response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return f"File {file_key} successfully written to bucket {bucket_name}"
    
    except ClientError as e:
        error_handler(e)

        raise ClientError(e.response, e.operation_name)
