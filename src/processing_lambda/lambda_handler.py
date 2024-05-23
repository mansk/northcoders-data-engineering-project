import logging
import datetime

if __name__ == "lambda_handler":
    from utils.write_object_to_s3_bucket import write_object_to_s3_bucket
    from utils.filter_dataframe import (
        filter_and_convert_dataframe_to_parquet,
    )
    from utils.read_ingestion_object_to_df import (
        read_object_into_dataframe,
    )
    from utils.create_dim_design_transaction_payment import drop_update_created_at_two_columns
else: 
    from src.processing_lambda.utils.write_object_to_s3_bucket import write_object_to_s3_bucket
    from src.processing_lambda.utils.filter_dataframe import (
        filter_and_convert_dataframe_to_parquet,
    )
    from src.processing_lambda.utils.read_ingestion_object_to_df import (
        read_object_into_dataframe,
    )
    from src.processing_lambda.utils.create_dim_design_transaction_payment import drop_update_created_at_two_columns

def transformation_function(data):
    return data

def lambda_handler(event, context):
    """Process JSON Lines files from the ingestion bucket and write transformed data to the processed bucket."""

    curr_timestamp = datetime.datetime.now(datetime.UTC)
    curr_timestamp_string = curr_timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    table_name = key.split("/")[0]

    logger.info(f"Processing file {key} from bucket {bucket_name}")

    try:
        ingested_data_frame = read_object_into_dataframe(bucket_name, key)
    except Exception as e:
        logger.error(f"Error reading data from ingestion bucket into dataframe: {e}")
        return

    if table_name == "address":
        df = transformation_function(ingested_data_frame)
    elif table_name == "counterparty":
        df = transformation_function(ingested_data_frame)
    elif table_name == "currency":
        df = transformation_function(ingested_data_frame)
    elif table_name == "department":
        df = transformation_function(ingested_data_frame)
    elif table_name == "design":
        df = drop_update_created_at_two_columns(ingested_data_frame)
    elif table_name == "payment_type":
        df = transformation_function(ingested_data_frame)
    elif table_name == "payment":
        df = transformation_function(ingested_data_frame)
    elif table_name == "purchase_order":
        df = transformation_function(ingested_data_frame)
    elif table_name == "sales_order":
        df = transformation_function(ingested_data_frame)
    elif table_name == "staff":
        df = transformation_function(ingested_data_frame)
    elif table_name == "transaction":
        df = transformation_function(ingested_data_frame)

    df_columns = df.columns.tolist()

    parquet_data = filter_and_convert_dataframe_to_parquet(df, df_columns)

    processed_bucket = "de-watershed-processed-bucket"

    try:
        write_object_to_s3_bucket(
            processed_bucket,
            f"{table_name}/{curr_timestamp_string}.parquet",
            parquet_data,
            binary=True,
        )

        logger.info(
            f"Successfully processed and wrote file to s3://{processed_bucket}/{table_name}"
        )

    except Exception as e:
        logger.error(f"Error writing parquet data to processed s3 bucket: {e}")
