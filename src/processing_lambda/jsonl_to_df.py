import boto3
import pandas as pd
import io
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")
tables = ["counterparty", "currency", "department", "design", "staff", "sales_order", "address", "payment", "purchase_order", "payment_type","transaction"]

def get_objects_from_s3_bucket(table_name):
   """
   Retrieves and concatenates JSON Lines files into a single DataFrame.
    This function lists all objects in the specified S3 bucket with the given prefix (table_name),
    reads each object as a JSON Lines file, and concatenates the contents into a single Pandas DataFrame.
    Args:
        table_name: A string representing the prefix of the objects(table name) to retrieve from the S3 bucket.
    Returns:
        A Pandas DataFrame containing the concatenated data from all the JSON Lines in the table.
    Raises:
        ClientError: If there's an issue with accessing the S3 bucket or its contents.
    """
    df = pd.DataFrame()
    try:
        objects=s3_client.list_objects_v2(Bucket="de-watershed-ingestion-bucket",
        Prefix=table_name).get('Contents',[])
        for obj in objects:
            file = s3_client.get_object(Bucket="de-watershed-ingestion-bucket", Key=obj['Key'])
            content=file['Body'].read().decode('utf-8')
            obj_df = pd.read_json(io.StringIO(content), lines=True)
            df = pd.concat([df, obj_df], ignore_index=True)
        return df
    except ClientError as e:
        raise ClientError(e.response, e.operation_name)
   
for table in tables:
    get_objects_from_s3_bucket(table)









