import os
import json
import boto3
import pytest
from moto import mock_aws
from src.processing_lambda.lambda_handler import lambda_handler
import datetime

@pytest.fixture(scope="function")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture
def s3_client(aws_creds):
    with mock_aws():
        yield boto3.client("s3")

@pytest.fixture
def s3_bucket(s3_client):
    bucket_name = 'test-bucket'
    region = 'eu-west-2'
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
    return bucket_name

@pytest.fixture
def s3_processed_bucket(s3_client):
    bucket_name = 'test-processed-bucket'
    region = 'eu-west-2'
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
    return bucket_name

@pytest.fixture
def add_bucket_object(s3_client, s3_bucket):
    json_data = b'{"col1": 1, "col2": "value1", "col3": true}\n' \
                b'{"col1": 2, "col2": "value2", "col3": false}\n' \
                b'{"col1": 3, "col2": "value3", "col3": true}'

    key = "address/sample.jsonl"
    s3_client.put_object(Bucket=s3_bucket, Key=key, Body=json_data)
    return key

@pytest.fixture
def event(s3_bucket):
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": s3_bucket,
                        "arn": f"arn:aws:s3:::{s3_bucket}"
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

def test_lambda_handler(s3_client, s3_bucket, s3_processed_bucket, add_bucket_object, event):
    lambda_handler(event, None)

    # Assuming you have assertions to check if the data is processed correctly and written to the processed bucket
    # For simplicity, you can just check if the object is present in the processed bucket
    response = s3_client.list_objects_v2(Bucket=s3_processed_bucket)
    assert 'Contents' in response
    assert len(response['Contents']) == 1
    assert response['Contents'][0]['Key'] == "address/sample.parquet"

