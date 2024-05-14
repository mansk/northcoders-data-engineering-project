import boto3
from botocore.exceptions import ClientError
import json
'''
To access db creds using the function
Database = get_database_credentials()["database"]
Hostname = get_database_credentials()["hostname"]
Username = get_database_credentials()["username"]
Password = get_database_credentials()["password"]
Port = get_database_credentials()["port"]
'''
def get_database_credentials():
    sm_client = boto3.client(
        "secretsmanager"
    )
    try:
        response = sm_client.get_secret_value(SecretId="database_credentials")
        db_creds = response["SecretString"]
        json_creds = json.loads(db_creds)
        return json_creds
    except ClientError as e:
        raise e
