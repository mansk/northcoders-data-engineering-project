import boto3
import pandas as pd
import io

def read_object_to_dataframe(bucket_name, key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    body = response['Body'].read()
    df = pd.read_json(io.BytesIO(body), lines=True)
    return df