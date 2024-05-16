import boto3
from botocore.exceptions import ClientError
import json

"""
To access db creds using the function:

Pass secret_id e.g. "database_credentials" or "warehouse_credentials"
to the get_database_credentials function - this way we can reuse the
function when we need to access the warehouse in the future.

Database = get_database_credentials()["database"]
Hostname = get_database_credentials()["hostname"]
Username = get_database_credentials()["username"]
Password = get_database_credentials()["password"]
Port = get_database_credentials()["port"]
"""


def get_database_credentials(secret_id):
    sm_client = boto3.client("secretsmanager")
    try:
        response = sm_client.get_secret_value(SecretId=secret_id)
        db_creds = response["SecretString"]
        json_creds = json.loads(db_creds)
        return json_creds
    except ClientError as e:
        raise e
