import boto3
from botocore.exceptions import ClientError

try:
    from utils.custom_exceptions import *
except ModuleNotFoundError:
    from src.custom_exceptions import *


def get_parameter(param: str):
    ssm_client = boto3.client("ssm")

    try:
        response = ssm_client.get_parameter(Name=param)

        return response["Parameter"]["Value"]

    except ClientError as e:
        error_handler(e)

        raise ClientError(e.response, e.operation_name)


def set_parameter(param: str, value: str):
    ssm_client = boto3.client("ssm")

    try:
        ssm_client.put_parameter(Name=param, Value=value, Type="String", Overwrite=True)

    except ClientError as e:
        error_handler(e)

        raise ClientError(e.response, e.operation_name)
