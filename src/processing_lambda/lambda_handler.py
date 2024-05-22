import logging
from src.write_object_to_s3_bucket import write_object_to_s3_bucket
from src.processing_lambda.utils.filter_dataframe import filter_and_convert_dataframe_to_parquet
from src.processing_lambda.utils.read_ingestion_object_to_df import read_object_into_dataframe
import datetime

def transformation_function(data):
    pass

def lambda_handler(event, context):
    """Process JSON Lines files from the ingestion bucket and write transformed data to the processed bucket."""

    curr_timestamp = datetime.datetime.now(datetime.UTC)
    curr_timestamp_string = curr_timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    table_name = key.split('/')[0]  

    logger.info(f"Processing file {key} from bucket {bucket_name}")

    ingested_data_frame = read_object_into_dataframe(bucket_name, key)

    if table_name == 'address':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'counterparty':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'currency':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'department':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'design':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'payment_type':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'payment':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'purchase_order':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'sales_order':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'staff':
        df = transformation_function(ingested_data_frame)
    elif table_name == 'transaction':
        df = transformation_function(ingested_data_frame)

    df_columns = df.columns.tolist()

    parquet_data = filter_and_convert_dataframe_to_parquet(df, df_columns)

    processed_bucket = "de-watershed-processed-bucket"

    write_object_to_s3_bucket(Bucket=processed_bucket, Key=f"{table_name}/{curr_timestamp_string}.parquet", Data=parquet_data, Binary=True)

    logger.info(f"Successfully processed and wrote file to s3://{processed_bucket}/{table_name}")

# IGNORE tests for now - need to restructure as the not sure the lambda handler is finished.