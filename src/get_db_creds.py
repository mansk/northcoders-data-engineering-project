import boto3
from botocore.exceptions import ClientError
import json
def get_database_credentials(secret_id):
    """Retrieves database credentials from AWS secrets manager.

    This function retrieves database credentials from the AWS secrets manager.
    We are using it to retrieve login credentials for the database we are ingesting from and the warehouse we are loading into.

    Args:
        secret_id: The relevant secret_id is passed into the function as a string to retrieve credentials for the specified secret.

    Returns:
        Credentials in json format, accessible by key e.g.
        Database = get_database_credentials("db_secret_id")["database"]
        Hostname = get_database_credentials("db_secret_id")["hostname"]
        Username = get_database_credentials("db_secret_id")["username"]
        Password = get_database_credentials("db_secret_id")["password"]
        Port = get_database_credentials("db_secret_id")["port"]
    """
    sm_client = boto3.client("secretsmanager")
    try:
        response = sm_client.get_secret_value(SecretId=secret_id)
        db_creds = response["SecretString"]
        json_creds = json.loads(db_creds)
        return json_creds
    except ClientError as e:
        raise e
