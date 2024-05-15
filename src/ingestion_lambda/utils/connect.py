import pg8000.native
import os
from dotenv import load_dotenv
from src.get_db_creds import get_database_credentials

load_dotenv()
os.environ["PG_USER"] = get_database_credentials()["username"]
os.environ["PG_PASSWORD"] = get_database_credentials()["password"]
os.environ["PG_DATABASE"] = get_database_credentials()["database"]
os.environ["PG_HOST"] = get_database_credentials()["hostname"]
os.environ["PG_PORT"] = str(get_database_credentials()["port"])


def connect_db():
    return pg8000.native.Connection(
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        database=os.getenv("PG_DATABASE"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
    )
