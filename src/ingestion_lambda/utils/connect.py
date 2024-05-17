import pg8000.native
import os

# from dotenv import load_dotenv
try:
    from utils.get_db_creds import get_database_credentials
except ModuleNotFoundError:
    from src.ingestion_lambda.utils.get_db_creds import get_database_credentials

# load_dotenv()


def connect_db() -> pg8000.native.Connection:
    """Connects to a PostgreSQL database using pg8000.

    This function uses the get_database_credentials function (with the arg
    "database_credentials") to retrieve the necessary credentials

    Args:
        None.

    Returns:
        An instance of the pg8000.native.Connection class.
    """
    return pg8000.native.Connection(
        user=get_database_credentials("database_credentials")["username"],
        password=get_database_credentials("database_credentials")["password"],
        database=get_database_credentials("database_credentials")["database"],
        host=get_database_credentials("database_credentials")["hostname"],
        port=str(get_database_credentials("database_credentials")["port"]),
    )
