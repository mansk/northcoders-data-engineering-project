import boto3
from botocore.exceptions import ClientError
import datetime
import json
import logging
from .utils.connect import connect_db
from .utils.get_table import get_table
from .utils.convert_results_to_json_lines import convert_results_to_json_lines
from .utils.custom_exceptions import *
from .utils.write_object_to_s3_bucket import write_object_to_s3_bucket
from .utils.ssm import get_parameter, set_parameter

client = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TIMESTAMP_PARAM = 'timestamp_of_last_successful_execution'


def lambda_handler():

    curr_timestamp = datetime.datetime.now(datetime.UTC)
    curr_timestamp_string = curr_timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    try:
        last_timestamp = get_parameter(TIMESTAMP_PARAM)
        last_timestamp = datetime.datetime.fromisoformat(last_timestamp)

    except ParameterNotFound:
        last_timestamp = datetime.datetime.min

    except ClientError:
        error_handler(e)

        raise ClientError(e.response, e.operation_name)

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
            results[table] = get_table(table, conn, last_timestamp)
            logger.info(f'get_table ran successfully on table \'{table}\'')
        except Exception as e:
            logger.error(e)

    for table in results:
        if results[table]:
            output[table] = convert_results_to_json_lines(results[table])

    for table in output:
        write_object_to_s3_bucket(
            'de-watershed-ingestion-bucket',
            f'{table}/{curr_timestamp_string}.jsonl',
            output[table]
        )

    set_parameter(TIMESTAMP_PARAM, curr_timestamp.isoformat())
