import os
import json
import boto3
import pytest
from moto import mock_aws
from src.processing_lambda.lambda_handler import lambda_handler

@pytest.fixture(scope="function")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture(scope="function")
def s3_client(aws_creds):
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")  
        yield s3

def event():
    event = {
    "Records": [
        {
        "s3": {
            "bucket": {
            "name": "de-watershed-ingestion-bucket",
            "arn": "arn:aws:s3:::de-watershed-ingestion-bucket"
            },
            "object": {
            "key": "address/sample.jsonl",
            "size": 1024,
            "eTag": "0123456789abcdef0123456789abcdef",
            "sequencer": "0123456789ABCDEF"
            }
        }
        }
    ]
    }
    return event