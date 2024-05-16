import pg8000.native
import os
# from dotenv import load_dotenv
from utils.get_db_creds import get_database_credentials

# load_dotenv()


def connect_db():
    return pg8000.native.Connection(
        user=get_database_credentials("database_credentials")["username"],
        password=get_database_credentials("database_credentials")["password"],
        database=get_database_credentials("database_credentials")["database"],
        host=get_database_credentials("database_credentials")["hostname"],
        port=str(get_database_credentials("database_credentials")["port"])
    )
