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
    from utils.create_dim_staff import create_dim_staff
    from utils.create_dim_counterparty import create_dim_counterparty
    from utils.create_dim_currency import create_dim_currency
    from utils.create_dim_date import create_dim_date
    from utils.create_dim_location import create_dim_location
    from utils.create_fact_sales_order import create_fact_sales_order, LAST_SALES_RECORD_ID_PARAM
    from utils.ssm import set_parameter
else: 
    from src.processing_lambda.utils.write_object_to_s3_bucket import write_object_to_s3_bucket
    from src.processing_lambda.utils.filter_dataframe import (
        filter_and_convert_dataframe_to_parquet,
    )
    from src.processing_lambda.utils.read_ingestion_object_to_df import (
        read_object_into_dataframe,
    )
    from src.processing_lambda.utils.create_dim_design_transaction_payment import drop_update_created_at_two_columns
    from src.processing_lambda.utils.create_dim_staff import create_dim_staff
    from src.processing_lambda.utils.create_dim_counterparty import create_dim_counterparty
    from src.processing_lambda.utils.create_dim_currency import create_dim_currency
    from src.processing_lambda.utils.create_dim_date import create_dim_date
    from src.processing_lambda.utils.create_dim_location import create_dim_location
    from src.processing_lambda.utils.create_fact_sales_order import create_fact_sales_order, LAST_SALES_RECORD_ID_PARAM
    from src.processing_lambda.utils.ssm import set_parameter



def lambda_handler(event, context):
    """Process JSON Lines files from the ingestion bucket and write transformed data to the processed bucket.
    """

    table_prefixes = {"address": "dim_location",
                      "counterparty": "dim_counterparty",
                      "staff": "dim_staff",
                      "currency": "dim_currency",
                      "design": "dim_design",
                      "payment_type": "dim_payment_type",
                      "payment": "fact_payment",
                      "purchase_order": "fact_purchase_order",
                      "sales_order" : "fact_sales_order",
                      "transaction" : "dim_transaction"}

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
    
    date_df = None

    if table_name == "address":
        df = create_dim_location(ingested_data_frame)
    elif table_name == "counterparty":
        df = create_dim_counterparty(ingested_data_frame)
    elif table_name == "currency":
        df = create_dim_currency(ingested_data_frame)
    elif table_name == "design":
        df = drop_update_created_at_two_columns(ingested_data_frame)
    elif table_name == "payment_type":
        df = drop_update_created_at_two_columns(ingested_data_frame)
    elif table_name == "payment":
        logging.info(f"Skipping data for table {table_name}")
        return None
    elif table_name == "purchase_order":
        logging.info(f"Skipping data for table {table_name}")
        return None
    elif table_name == "sales_order":
        df, date_df = create_fact_sales_order(ingested_data_frame)
    elif table_name == "staff":
        df = create_dim_staff(ingested_data_frame)
    elif table_name == "transaction":
        df = drop_update_created_at_two_columns(ingested_data_frame)
    elif table_name == "department":
        logging.info(f"Skipping data for table {table_name}")
        return None
    else:
        logging.error(f"New table: {table_name} found")
        return None

    df_columns = df.columns.tolist()

    parquet_data = filter_and_convert_dataframe_to_parquet(df, df_columns)

    if date_df is not None:
        date_df_columns = date_df.columns.tolist()
        date_parquet_data = filter_and_convert_dataframe_to_parquet(date_df, date_df_columns)


    processed_bucket = "de-watershed-processed-bucket"

    try:
        write_object_to_s3_bucket(
            processed_bucket,
            f"{table_prefixes[table_name]}/{curr_timestamp_string}.parquet",
            parquet_data,
            binary=True,
        )

        logger.info(
            f"Successfully processed and wrote file to s3://{processed_bucket}/{table_prefixes[table_name]}"
        )

        if table_name == "sales_order":
            set_parameter(LAST_SALES_RECORD_ID_PARAM, str(df["sales_record_id"].max()))

        if date_df is not None:
            write_object_to_s3_bucket(
                processed_bucket,
                f"dim_date/{curr_timestamp_string}.parquet",
                date_parquet_data,
                binary=True,
            )

            logger.info(
                f"Successfully processed and wrote file to s3://{processed_bucket}/dim_date"
            )


    except Exception as e:
        logger.error(f"Error writing parquet data to processed s3 bucket: {e}")
