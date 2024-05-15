import boto3
import datetime
import json
import logging
from .utils.connect import connect_db
from .utils.get_table import get_table
from .utils.convert_results_to_json_lines import convert_results_to_json_lines

client = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler():
    timestamp = datetime.datetime.now()
    timestamp_string = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    #Check S3 bucket for timestamp of last successful execution?

    tables = [
        "counterparty", "currency", "department", "design", "staff",
        "sales_order", "address", "payment", "purchase_order", "payment_type",
        "transaction"
        ]

    conn = None

    results = {}
    output = {}

    try:
        conn = connect_db()
    except Exception as e:
        logger.error(e)

    for table in tables:
        try:
            results[table] = get_table(table, conn)
            logger.info(f'get_table ran successfully on table \'{table}\'')
        except Exception as e:
            logger.error(e)

    for table in results:
        if results[table]:
            output[table] = convert_results_to_json_lines(results[table])


    #Create file in S3 bucket with filename equal to timestamp string?
